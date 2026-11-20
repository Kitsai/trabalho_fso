from enum import Enum
from threading import Semaphore

from process_module import Process


class Resource(Enum):
    PRINTER = 0
    SCANNER = 1
    MODEM = 2
    SATA = 3


RESOURCE_CAPACITY = {
    Resource.PRINTER: 2,
    Resource.SCANNER: 1,
    Resource.MODEM: 1,
    Resource.SATA: 2,
}


class IoManager:
    def __init__(self) -> None:
        self._semaphores = {
            resource: Semaphore(capacity)
            for resource, capacity in RESOURCE_CAPACITY.items()
        }

    def allocate(self, process: Process) -> bool:
        acquired: list[Resource] = []

        for resource in self._required_resources(process):
            if self._semaphores[resource].acquire(blocking=False):
                acquired.append(resource)
            else:
                self._rollback(acquired)
                return False

        return True

    def release(self, process: Process) -> None:
        for resource in self._required_resources(process):
            self._semaphores[resource].release()

    def _rollback(self, acquired: list[Resource]) -> None:
        for resource in acquired:
            self._semaphores[resource].release()

    @staticmethod
    def _required_resources(process: Process) -> list[Resource]:
        requested = {
            Resource.PRINTER: process.printer_req,
            Resource.SCANNER: process.scanner_req,
            Resource.MODEM: process.modem_req,
            Resource.SATA: process.sata_req,
        }
        return [resource for resource in Resource if requested[resource]]
