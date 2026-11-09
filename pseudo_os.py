import queue
import queues_module
from resources_module import IoManager
import sys

from memory_module import MemoryManager
from files_module import FilesManager
from queues_module import QueuesManager


class PseudoOs:
    def __init__(self, processes: str, operations: str, strings: str):
        self.queues = QueuesManager(processes)
        self.files = FilesManager()
        self.io = IoManager()
        self.memory = MemoryManager()

        self.clock = 0
        self.finished = False

    def run(self):
        while not self.finished:
            self.queues.tick(self.clock)

            self.clock += 1


if __name__ == "__main__":
    argc = len(sys.argv) - 1

    if argc < 3:
        print("You need to pass 3 files on this order:")
        print(
            "python pseudo_os.py <process infos> <file operations> <page ref strings>"
        )
        sys.exit(1)

    processes = sys.argv[1]
    operations = sys.argv[2]
    strings = sys.argv[3]

    os = PseudoOs(processes, operations, strings)

    os.run()
