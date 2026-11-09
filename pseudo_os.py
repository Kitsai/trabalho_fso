import sys

from process_module import ProcessesManager
from memory_module import MemoryManager
from files_module import FilesManager
from queues_module import QueuesManager
from resources_module import ResourcesManager


class PseudoOs:
    def __init__(self):
        self.files = FilesManager()
        self.resources = ResourcesManager()
        self.memory = MemoryManager()
        self.processes = ProcessesManager()
        self.queues = QueuesManager()

    def run(self):
        print("Running simulator")
        self.files.run()
        self.resources.run()
        self.memory.run()
        self.processes.run()
        self.queues.run()


if __name__ == "__main__":
    argc = len(sys.argv) - 1

    if argc < 3:
        print(f"You need to pass 3 files on this order:")
        print(
            f"python pseudo_os.py <process infos> <file operations> <page ref strings>"
        )
        sys.exit(1)

    print(f"Args {sys.argv[1:]}")

    os = PseudoOs()

    os.run()
