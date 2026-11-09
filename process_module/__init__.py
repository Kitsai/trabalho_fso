class Process:
    id = 0

    def __init__(self) -> None:
        self.id = Process.id
        Process.id += 1


class ProcessesManager:
    def run(self):
        print("Running proccess manager")
