from state import State
from tools.base import Tool, ToolExample

class WeekdayTool(Tool):
    def __init__(self):
        super().__init__(
            name="WEEKDAY",
            description="Gets the week day for a given date.",
            examples=[
                ToolExample(
                    input="What day of the week was 2023-03-03?",
                    output="The date 2023-03-03 is a [WEEKDAY(2023-03-03) -> Thursday] Thursday."
                ),
                ToolExample(
                    input="Is today a Friday?",
                    output="Today's date is [NOW() -> 2023-03-03 03:19:47.980140] 2023-03-03, which is a [WEEKDAY(2023-03-03) -> Thursday] Thursday, not a Friday."
                ),
                ToolExample(
                    input="What day will it be tomorrow?",
                    output="Today's date is [NOW() -> 2023-03-04 03:19:47.125423] 2023-03-04, which means tomorrow will be 2023-03-05, which is a [WEEKDAY(2023-03-05) -> Sunday] Sunday."
                )
            ],
            method=self.invoke
        )

    def invoke(self, state: State, datestr: str, *args, **kwargs) -> str:
        import datetime
        # Convert date string to datetime object
        date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d')

        # Get weekday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        weekday = date_obj.weekday()

        # Convert weekday integer to weekday name
        weekday_name = datetime.date(1900, 1, 1 + weekday).strftime("%A")
        return weekday_name