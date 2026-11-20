from dataclasses import dataclass


@dataclass
class ProcessData:
    start_time: int
    priority: int
    process_time: int
    workset_size: int
    printer_req: bool
    scanner_req: bool
    modem_req: bool
    sata_req: bool


@dataclass
class FileData:
    file_name: str
    first_block: int
    block_count: int


@dataclass
class FileOperationData:
    process_id: int
    op_code: int
    file_name: str
    create_blocks: int | None


@dataclass
class FilesInputContext:
    total_blocks: int
    occupied_blocks: int
    files: list[FileData]
    operations: list[FileOperationData]


@dataclass
class InputContext:
    processes: list[ProcessData]
    files_ctx: FilesInputContext
    page_requests: list[list[int]]


def read_input(processes_path: str, files_path: str, strings_path: str) -> InputContext:
    return InputContext([], FilesInputContext(0, 0, [], []), [])
