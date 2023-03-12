from dataclasses import dataclass, field
from typing import *
from client_types import Message
import lifecycle
import websockets
import asyncio
from enum import Enum

class Mode(Enum):
    ACTIVATION_KEYWORD = 0
    ALWAYS_ON = 1

@dataclass
class State:
    message_history: List[Message] = field(default_factory=list)
    connected_clients: Set[websockets.WebSocketServerProtocol] = field(default_factory=set)
    mode: Mode = Mode.ACTIVATION_KEYWORD,
    stop_future: asyncio.Future = field(default_factory=lifecycle.create_lifecycle)
    predict_queue: asyncio.Queue[Tuple[str,str]] = asyncio.Queue()
    predict_reply_queue: asyncio.Queue[str] = asyncio.Queue()
    voice_queue: asyncio.Queue[str] = asyncio.Queue()
    
    async def predict(self, prompt: str, stop_token: str) -> str:
        # print(f"[PREDICT] Sending prompt to queue: {prompt}")
        await self.predict_queue.put((prompt, stop_token))
        reply = await self.predict_reply_queue.get()
        # print(f"[PREDICT] Got reply from queue: {reply}")
        return reply