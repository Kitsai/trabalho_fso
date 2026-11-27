from dataclasses import dataclass

from constants import MAX_PRIORITY


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
    occupied_segments: int
    files: list[FileData]
    operations: list[FileOperationData]


@dataclass
class InputContext:
    processes: list[ProcessData]
    files_ctx: FilesInputContext
    page_requests: list[list[int]]


def _parse_process(line: str) -> ProcessData:
    """Faz o parse de uma linha de um processo.

    Args:
        line: Conteudo que deve ser parseado para criar o processo

    Returns:
        O processo criado seguindo as especificações
    """
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

    return ProcessData(
        start_time=int(start_time),
        priority=priority,
        process_time=int(process_time),
        workset_size=int(workset_size),
        printer_req=bool(int(printer_req)),
        scanner_req=bool(int(scanner_req)),
        modem_req=bool(int(modem_req)),
        sata_req=bool(int(sata_req)),
    )


def read_processes(path: str) -> list[ProcessData]:
    with open(path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    return [_parse_process(line) for line in lines]


def parse_file(line: str) -> FileData:
    (file_name, first_block, block_count) = (field.strip() for field in line.split(","))

    return FileData(
        file_name=file_name,
        first_block=int(first_block),
        block_count=int(block_count),
    )


def parse_file_operation(line: str) -> FileOperationData:
    fields = [field.strip() for field in line.split(",")]

    process_id = int(fields[0])
    op_code = int(fields[1])
    file_name = fields[2]

    if op_code == 0:
        if len(fields) != 4:
            raise ValueError("Create operations expects number of blocks to allocate")
        create_blocks = int(fields[3])
    elif op_code == 1:
        create_blocks = None
    else:
        raise ValueError("Available operations are 0 to create and 1 to delete")

    return FileOperationData(
        process_id=process_id,
        op_code=op_code,
        file_name=file_name,
        create_blocks=create_blocks,
    )


def read_files(path: str) -> FilesInputContext:
    with open(path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    total_blocks = int(lines[0].strip())
    occupied_segments = int(lines[1].strip())
    files = [parse_file(line) for line in lines[2 : 2 + occupied_segments]]
    operations = [parse_file_operation(line) for line in lines[2 + occupied_segments :]]

    return FilesInputContext(total_blocks, occupied_segments, files, operations)


def get_pages(line: str) -> list[int]:
    return [int(page.strip()) for page in line.split(",")]


def read_strings(path: str) -> list[list[int]]:
    with open(path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    return [get_pages(line) for line in lines]


def read_input(processes_path: str, files_path: str, strings_path: str) -> InputContext:
    return InputContext(
        read_processes(processes_path),
        read_files(files_path),
        read_strings(strings_path),
    )
