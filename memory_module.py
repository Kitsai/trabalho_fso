from dataclasses import dataclass

from constants import RT_TOTAL_FRAMES, USER_TOTAL_FRAMES
from process_module import Process


@dataclass
class MemoryManager:
    rt_frames: int = 0
    user_frames: int = 0

    def run(self):
        print("Running memory manager")

    def allocate(self, process: Process) -> bool:
        if (
            process.priority == 0
            and self.rt_frames + process.workset_size <= RT_TOTAL_FRAMES
        ):
            self.rt_frames += process.workset_size
            return True
        elif (
            process.priority > 0
            and self.user_frames + process.workset_size <= USER_TOTAL_FRAMES
        ):
            self.user_frames += process.workset_size
            return True

        return False

    def release(self, process: Process):
        if process.priority == 0 and self.rt_frames - process.workset_size >= 0:
            self.rt_frames -= process.workset_size
        elif self.user_frames - process.workset_size >= 0:
            self.user_frames -= process.workset_size
