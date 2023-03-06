import asyncio
import signal
from typing import *
def create_lifecycle(callback: Callable | None = None):
    stop_future = asyncio.get_running_loop().create_future()
    def shutdown(*args):
        print("[LIFECYCLE] Shutting down")
        stop_future.set_result(None)
        if callback is not None:
            callback()
        print("[LIFECYCLE] Shutdown complete")
    signal.signal(signal.SIGINT, shutdown)
    return stop_future