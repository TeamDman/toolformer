from tools.base import Tool, ToolExample
from state import State, Mode

class ModeTool(Tool):
    def __init__(self):
        super().__init__(
            name="MODE",
            description="Switches voice modes.",
            examples=[
                ToolExample(
                    input="Activation mode",
                    output="[MODE(ACTIVATION_KEYWORD) -> 0] Switched to activation keyword mode."
                ),
                ToolExample(
                    input="Always on mode",
                    output="[MODE(ALWAYS_ON) -> 0] Switched to always-on mode."
                ),
            ],
            method=self.invoke
        )

    def invoke(self, state: State, newMode: str) -> str:
        state.mode = Mode.__members__[newMode]
        return str(0)