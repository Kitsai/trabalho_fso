from collections import deque

from constants import MAX_PRIORITY
from input import InputContext
from process_module import Process, ProcessState


class QueuesManager:
    QUANTUM = 1  # quantum de um ms ou uma unidade de tempo logico

    """ Ticks até que o processo receba uma maior prioridade """
    AGING_THRESHOLD = 20

    def __init__(self, ctx: InputContext) -> None:
        """Cria 1 queue de tempo real e 3 de usuário, uma queue dos processos prontos e uma queue para orquestração dos processos inicializando

        A queue de pronto simplifica o acesso
        """
        self.real_time_queue: deque[int] = deque()
        self.user_queues: list[deque[int]] = [deque(), deque(), deque()]
        self.arrived_queue: deque[int] = deque()

        self.pcb_table: dict[int, Process] = {}

        self.initializing_queue: deque[Process] = deque()

        self.load_processes(ctx)

    def get_process(self, pid: int) -> Process | None:
        return self.pcb_table.get(pid)

    def load_processes(self, ctx: InputContext) -> None:
        """Cria Processos com base no arquivo passado

        Args:
            path: Caminho para arquivo com detalhes de cada processo
        """
        Process.reset_ids()

        processes = [Process(data) for data in ctx.processes]

        self.initializing_queue.extend(sorted(processes, key=lambda p: p.start_time))


    def tick(self, current_tick: int):
        """Interface padrão dos elementos que dependem do tempo lógico

        Args:
            current_tick: tick atual da simulação
        """
        self.update_queues(current_tick)

    def update_queues(self, current_tick: int) -> None:
        """Verifica processos que chegaram agora e ajusta prioridade com idade.

        Args:
            current_tick: tick atual da simulação
        """
        self._update_initialization(current_tick)
        self._update_arrived(current_tick)

        self._age_waiting_processes(current_tick)

    def _update_initialization(self, current_tick: int):
        while (
            self.initializing_queue
            and self.initializing_queue[0].start_time == current_tick
        ):
            p = self.initializing_queue.popleft();
            self.pcb_table[p.pid] = p
            self.arrived_queue.append(p.pid)

    def _update_arrived(self, current_tick):
        cant_start = deque()
        while self.arrived_queue:
            p = self.pcb_table[self.arrived_queue.popleft()]

            # TODO: verifica se consegue alocar memoria

            p.state = ProcessState.Ready
            self._route(p, current_tick)

    def _age_waiting_processes(self, current_tick: int) -> None:
        """Verifica idade de cada processo para verificar se ele pode subir de prioridade

        Args:
            current_tick: tick atual da simulação
        """
        for i in range(1, MAX_PRIORITY):
            aged = []
            for pid in self.user_queues[i]:
                p = self.pcb_table[pid]
                if current_tick - p.waiting_since > QueuesManager.AGING_THRESHOLD:
                    aged.append(pid)

            for pid in aged:
                self.user_queues[i].remove(pid)
                p = self.pcb_table[pid]
                p.priority -= 1
                self._route(p, current_tick)

    def _route(self, process: Process, current_tick: int) -> None:
        """Roteia o processo para a fila final correta

        Args:
            process: processo que deve ser roteado
            current_tick: tick atual da simulação
        """
        process.waiting_since = current_tick

        if process.priority == 0:
            self.real_time_queue.append(process.pid)
        else:
            self.user_queues[process.priority - 1].append(process.pid)

    def next_process(self) -> Process | None:
        if self.real_time_queue:
            return self.pcb_table[self.real_time_queue.popleft()]

        for queue in self.user_queues:
            if queue:
                return self.pcb_table[queue.popleft()]

        return None

    def requeue(self, process: Process, current_tick: int) -> None:
        process.priority = min(process.priority + 1, MAX_PRIORITY)
        self._route(process, current_tick)

    def is_finished(self) -> bool:
        return (
            not self.initializing_queue
            and not self.arrived_queue
            and not self.real_time_queue
            and all(not queue for queue in self.user_queues)
        )
