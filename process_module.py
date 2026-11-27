from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from input import ProcessData


class ProcessState(Enum):
    New = 0
    Ready = 1
    Running = 2
    Blocked = 3
    Finished = 4


@dataclass
class Process:
    next_id: ClassVar[int] = 0

    pid: int
    priority: int
    process_time: int
    workset_size: int
    printer_req: bool
    scanner_req: bool
    modem_req: bool
    sata_req: bool
    waiting_since: int
    remaining_time: int
    instructions_run: int = 0

    state: ProcessState = ProcessState.New

    @classmethod
    def reset_ids(cls) -> None:
        cls.next_id = 0

    def __init__(self, data: ProcessData) -> None:
        self.pid = Process.next_id
        Process.next_id += 1

        self.start_time = data.start_time
        self.priority = data.priority
        self.process_time = data.process_time
        self.workset_size = data.workset_size
        self.printer_req = data.printer_req
        self.scanner_req = data.scanner_req
        self.modem_req = data.modem_req
        self.sata_req = data.sata_req

        self.waiting_since = data.start_time
        self.remaining_time = data.process_time
