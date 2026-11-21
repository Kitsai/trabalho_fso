from collections import deque

from constants import MAX_PRIORITY
from input import InputContext
from process_module import Process


class QueuesManager:
    QUANTUM = 1  # quantum de um ms ou uma unidade de tempo logico

    """ Ticks até que o processo receba uma maior prioridade """
    AGING_THRESHOLD = 20

    def __init__(self, ctx: InputContext) -> None:
        """Cria 1 queue de tempo real e 3 de usuário, uma queue dos processos prontos e uma queue para orquestração dos processos inicializando

        A queue de pronto simplifica o acesso
        """
        self.real_time_queue = deque[Process]()
        self.user_queues: list[deque[Process]] = [deque(), deque(), deque()]

        self.initializing_queue: deque[Process] = deque()

        self.load_processes(ctx)

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
        while (
            self.initializing_queue
            and self.initializing_queue[0].start_time == current_tick
        ):
            self._route(self.initializing_queue.popleft(), current_tick)

        self._age_waiting_processes(current_tick)

    def _age_waiting_processes(self, current_tick: int) -> None:
        """Verifica idade de cada processo para verificar se ele pode subir de prioridade

        Args:
            current_tick: tick atual da simulação
        """
        for i in range(1, MAX_PRIORITY):
            aged = []
            for p in self.user_queues[i]:
                if current_tick - p.waiting_since > QueuesManager.AGING_THRESHOLD:
                    aged.append(p)

            for p in aged:
                self.user_queues[i].remove(p)
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
            self.real_time_queue.append(process)
        else:
            self.user_queues[process.priority - 1].append(process)

    def next_process(self) -> Process | None:
        if self.real_time_queue:
            return self.real_time_queue.popleft()

        for queue in self.user_queues:
            if queue:
                return queue.popleft()

        return None

    def requeue(self, process: Process, current_tick: int) -> None:
        process.priority = min(process.priority + 1, MAX_PRIORITY)
        self._route(process, current_tick)

    def is_finished(self) -> bool:
        return (
            not self.initializing_queue
            and not self.real_time_queue
            and all(not queue for queue in self.user_queues)
        )
