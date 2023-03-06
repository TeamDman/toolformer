from client_types import Message
from typing import *

history: List[Message] = [
    Message(
        side= "right",
        content= "Hello",
        timestamp= "2023-03-06T04:11:00.902Z",
        senderName= "User",
    ),
    Message(
        side= "left",
        content= "Hello",
        timestamp= "2023-03-06T04:11:00.902Z",
        senderName= "Assistant",
    ),
]

async def track_message(msg: Message) -> None:
    history.append(msg)

async def get_history() -> List[Message]:
    return history