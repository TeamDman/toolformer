from dataclasses import dataclass

@dataclass
class Message:
    side: str
    content: str
    timestamp: int
    senderName: str
