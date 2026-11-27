from collections import deque
from dataclasses import dataclass
from threading import BoundedSemaphore


@dataclass
class Semaphore:
    _semaphore: BoundedSemaphore
    _block_queue: deque[int]

    def __init__(self, entries: int) -> None:
        self._semaphore = BoundedSemaphore(entries)
        self._block_queue = deque[int]()

    def up(self) -> int | None:
        if self._block_queue:
            pid = self._block_queue.popleft()
            return pid
        
        self._semaphore.release()
        return None

    def down(self, pid: int) -> bool:
        acquired = self._semaphore.acquire(blocking=False)

        if not acquired:
            self._block_queue.append(pid)

        return acquired
