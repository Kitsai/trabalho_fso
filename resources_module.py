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
    pass
