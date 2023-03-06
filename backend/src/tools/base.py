from typing import Callable, List
from dataclasses import dataclass

@dataclass(frozen=True)
class ToolExample:
    input: str
    output: str

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    examples: List[ToolExample]
    method: Callable[[str],str]