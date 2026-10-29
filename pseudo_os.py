from process_module import ProcessesManager
from memory_module import MemoryManager
from io_module import IoManager
from files_module import FilesManager
class PseudoOs:
    def __init__(self):
        self.files = FilesManager()
        self.io = IoManager()
        self.memory = MemoryManager()
        self.processes = ProcessesManager()

    def run(self):
        print("Running simulator")
        self.files.run()
        self.io.run()
        self.memory.run()
        self.processes.run()
