from state import State
from tools.base import Tool, ToolExample

class MathTool(Tool):
    def __init__(self):
        super().__init__(
            name="MATH",
            description="Evaluates a math expression. You should always use this tool to evaluate math expressions.",
            examples=[
                ToolExample(
                    input="What's 9 plus 10?",
                    output="9+10=[MATH(9+10) -> 19.0000000000000] 19."
                ),
                ToolExample(
                    input="2+2",
                    output="2+2=[MATH(2+2) -> 4.00000000000000] 4."
                ),
                ToolExample(
                    input="Three over two",
                    output="3/2=[MATH(3/2) -> 1.50000000000000] 1.5."
                ),
            ],
            method=self.invoke
        )

    def invoke(self, state: State, mathexpr: str) -> str:
        import sympy
        result = sympy.sympify(mathexpr).evalf()
        return str(result)
        