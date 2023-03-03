from tools.base import Tool, ToolExample

class NowTool(Tool):
    def __init__(self):
        super().__init__(
            name="NOW",
            description="Print the current time.",
            examples=[
                ToolExample(
                    input="What time is it?",
                    output="It is [NOW() -> 2021-07-23 11:51:08.123456] 11:51 AM."
                ),
                ToolExample(
                    input="What is the date?",
                    output="Today's date is [NOW() -> 2021-07-23 11:51:08.123456] Friday July 23rd, 2021 (2021-07-23)."
                ),
            ],
            method=self.invoke
        )

    def invoke(self, *args, **kwargs) -> str:
        import datetime
        return str(datetime.datetime.now())