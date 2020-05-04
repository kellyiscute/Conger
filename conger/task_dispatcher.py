from typing import Callable
from threading import Thread
from conger import delegator


class Process:
    def __init__(self, command: str, exit_callback: Callable = None):
        self.cmd = delegator.run(command, False)
        self.exited = False
        self.th = Thread(target=self._block_thread, args=(exit_callback, ), name='block')
        self.th.start()

    def _block_thread(self, callback: Callable):
        self.cmd.block()
        if callback is not None:
            callback()

    def kill(self):
        self.cmd.kill()
