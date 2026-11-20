import threading
from collections import deque
from dataclasses import dataclass


@dataclass
class Semaphore:
    _semaphore: threading.Semaphore
    _block_queue: deque[int]
