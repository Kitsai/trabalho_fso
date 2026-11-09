from collections import deque
from queue import Queue

from process_module import Process

MAX_PROCESSES = 1000
MAX_PRIORITY = 3  # 0 = tempo real, 1-3 = usuario


class QueuesManager:
    QUANTUM = 1
    AGING_THRESHOLD = 20  # ticks esperando antes de promover de prioridade

    def __init__(self, process_file: str) -> None:
        self.real_time_queue = deque[Process]()
        self.user_queue: list[deque[Process]] = [deque(), deque(), deque()]
        self.ready_queue: deque[Process] = deque()

        self.load_processes(process_file)

    def load_processes(self, path: str) -> None:
        Process.reset_ids()

        with open(path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        if len(lines) > MAX_PROCESSES:
            raise ValueError(
                f"{path} has {len(lines)} processes, max is {MAX_PROCESSES}"
            )

        processes = [self._parse_process(line) for line in lines]
        self.ready_queue.extend(sorted(processes, key=lambda p: p.start_time))

    @staticmethod
    def _parse_process(line: str) -> Process:
        (
            start_time,
            priority,
            process_time,
            workset_size,
            printer_req,
            scanner_req,
            modem_req,
            sata_req,
        ) = (field.strip() for field in line.split(","))

        priority = int(priority)
        if not 0 <= priority <= MAX_PRIORITY:
            raise ValueError(
                f"invalid priority {priority} in line '{line}': "
                f"must be 0 (tempo real) to {MAX_PRIORITY} (usuario)"
            )

        return Process(
            start_time=int(start_time),
            priority=priority,
            process_time=int(process_time),
            workset_size=int(workset_size),
            printer_req=bool(int(printer_req)),
            scanner_req=bool(int(scanner_req)),
            modem_req=bool(int(modem_req)),
            sata_req=bool(int(sata_req)),
        )

    def tick(self, current_tick: int):
        self.update_queues(current_tick)

    def update_queues(self, current_tick: int) -> None:
        while self.ready_queue and self.ready_queue[0].start_time == current_tick:
            self._route(self.ready_queue.popleft(), current_tick)

        self._age_waiting_processes(current_tick)

    def _route(self, process: Process, current_tick: int) -> None:
        process.waiting_since = current_tick

        if process.priority == 0:
            self.real_time_queue.append(process)
        else:
            self.user_queue[process.priority - 1].append(process)

    def _age_waiting_processes(self, current_tick: int) -> None:
        for level in range(1, len(self.user_queue)):
            queue = self.user_queue[level]
            still_waiting: deque[Process] = deque()

            while queue:
                process = queue.popleft()
                waiting_for = current_tick - process.waiting_since

                if waiting_for >= self.AGING_THRESHOLD:
                    process.priority -= 1
                    self._route(process, current_tick)
                else:
                    still_waiting.append(process)

            self.user_queue[level] = still_waiting

    def next_process(self) -> Process | None:
        if not self.real_time_queue:
            return self.real_time_queue.popleft()

        for queue in self.user_queue:
            if queue:
                return queue.popleft()

        return None

    def requeue(self, process: Process, current_tick: int) -> None:
        process.priority = min(process.priority + 1, len(self.user_queue))
        self._route(process, current_tick)

    def is_finished(self) -> bool:
        return (
            not self.ready_queue
            and not self.real_time_queue
            and all(not queue for queue in self.user_queue)
        )
