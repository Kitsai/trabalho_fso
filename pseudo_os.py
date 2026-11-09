import sys

from files_module import FilesManager
from memory_module import MemoryManager
from process_module import Process
from queues_module import QueuesManager
from resources_module import IoManager


class PseudoOs:
    def __init__(self, processes: str, operations: str, strings: str):
        self.queues = QueuesManager(processes)
        self.files = FilesManager()
        self.io = IoManager()
        self.memory = MemoryManager()

        self.clock = 0

    def run(self) -> None:
        current_process: Process | None = None

        while current_process is not None or not self.queues.is_finished():
            self.queues.tick(self.clock)

            if current_process is None:
                current_process = self.queues.next_process()
                if current_process is not None and not current_process.started:
                    self._announce(current_process)

            if current_process is not None:
                finished = self._run_instruction(current_process)

                if finished:
                    self._finish(current_process)
                    current_process = None
                elif current_process.priority != 0:
                    self.queues.requeue(current_process, self.clock)
                    current_process = None

            self.clock += 1

    def _announce(self, process: Process) -> None:
        print("dispatcher => ")
        print(f"    PID: {process.pid}")
        print(f"    frames: {process.workset_size}")
        print(f"    priority: {process.priority}")
        print(f"    time: {process.process_time}")
        print(f"    printers: {int(process.printer_req)}")
        print(f"    scanners: {int(process.scanner_req)}")
        print(f"    modems: {int(process.modem_req)}")
        print(f"    drives: {int(process.sata_req)}")

        # TODO: alocar recursos de I/O (self.io.allocate(process))

        print(f"process {process.pid} =>")
        print(f"P{process.pid} STARTED")
        process.started = True

    def _run_instruction(self, process: Process) -> bool:
        process.instructions_run += 1
        print(f"P{process.pid} instruction {process.instructions_run}")

        process.remaining_time -= 1
        return process.remaining_time == 0

    def _finish(self, process: Process) -> None:
        print(f"P{process.pid} return SIGINT")

        # TODO: liberar recursos de I/O (self.io.release(process))


if __name__ == "__main__":
    argc = len(sys.argv) - 1

    if argc < 3:
        print("You need to pass 3 files on this order:")
        print(
            "python pseudo_os.py <process infos> <file operations> <page ref strings>"
        )
        sys.exit(1)

    processes = sys.argv[1]
    operations = sys.argv[2]
    strings = sys.argv[3]

    os = PseudoOs(processes, operations, strings)

    os.run()
