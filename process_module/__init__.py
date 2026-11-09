class Process:
    next_id: int = 0

    @classmethod
    def reset_ids(cls) -> None:
        cls.next_id = 0

    def __init__(
        self,
        start_time: int,
        priority: int,
        process_time: int,
        workset_size: int,
        printer_req: bool,
        scanner_req: bool,
        modem_req: bool,
        sata_req: bool,
    ) -> None:
        self.pid = Process.next_id
        Process.next_id += 1

        self.start_time = start_time
        self.priority = priority
        self.process_time = process_time
        self.workset_size = workset_size
        self.printer_req = printer_req
        self.scanner_req = scanner_req
        self.modem_req = modem_req
        self.sata_req = sata_req

        self.waiting_since: int = start_time
        self.remaining_time: int = process_time
        self.instructions_run: int = 0
        self.started: bool = False
