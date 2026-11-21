from enum import Enum

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
    def allocate(self, process: Process) -> bool:
        """Tenta alocar recursos pedidos pelo processo.

        ao tentar alocar sempre tenta primeiro os recursos em ordem crescente (passivel de mudanca)

        Args:
            process: Processo que tenta alocar dispositivos
        Returns:
            bool: Indica se conseguiu alocar ou nao
        """
        return True
