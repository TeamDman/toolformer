from typing import *

from tools.now import NowTool
from tools.weekday import WeekdayTool
from tools.math import MathTool
from tools.snap import SnapTool

from tools.base import Tool
from text import predict

tools = [
    NowTool(),
    WeekdayTool(),
    MathTool(),
    SnapTool()
]

tools_dict = {tool.name: tool for tool in tools}

def handle_tool_invocation(response: str) -> Tuple[Literal[False], None] | Tuple[Literal[True],str]:
    # check for tool invocation and capture parameters
    try:
        import re
        pattern = r".*\[\s*(\w+)\((.*?)\)\s*->\s*"
        found = re.match(pattern, response, re.DOTALL)
        if found:
            tool_name = found.group(1)
            params = found.group(2)
            tool = get_tool(tool_name)
            if tool:
                result = tool.method(params)
                return True, result
    except Exception as e:
        return True, f"ERROR: {e}"
    return False, None

def predict_with_tools(prompt: str) -> Tuple[str, Any]:
    first_prompt = build_preprompt() + prompt + build_postprompt()
    first_response_raw = predict(first_prompt, "->")

    # trim agent over-continuing the conversation
    good, bad = (first_response_raw+"User:").split("User:", maxsplit=1)
    first_response = good
    
    tool_was_used, result = handle_tool_invocation(first_response)
    if tool_was_used:
        assert result is not None
        second_prompt = first_prompt + first_response + result + "]"
        second_response = predict(second_prompt, "\n")
        full_response = first_response + result + "]" + second_response
        return full_response, {
            "first_prompt": first_prompt,
            "first_response": first_response,
            "second_prompt": second_prompt,
            "second_response": second_response,
            "bad": bad,
        }
        
    else:
        return first_response, {
            "first_prompt": first_prompt,
            "first_response": first_response,
        }

def get_tool(tool_name: str) -> Tool:
    return tools_dict[tool_name]

def build_postprompt() -> str:
    return "Assistant:"

def build_preprompt() -> str:
    prompt = "You are an AI assistant with several tools available to you. The tools are the following:\n"
    # list tool definitions
    for tool in tools:
        prompt += f"{tool.name}: {tool.description}\n"
    prompt += (
        "\n"
        "DO NOT USE TOOLS WITHIN TOOLS! KEEP ALL TOOL CALLS SEPARATE FROM EACH OTHER!"
        "\n"
        "YOU ARE ENCOURAGED TO USE TOOLS TO ENSURE THE ACCURACY OF YOUR RESPONSES!"
        "\n"
        "YOU ARE TO EXPLAIN YOUR REASONING AND SHOW YOUR WORK, WITH CLEAR CONNECTIONS BETWEEN CONCLUSIONS!"
        "\n"
        "DO NOT PUT A LINE BREAK BEFORE A TOOL CALL!"
        "\n\n"
    )

    # list examples
    for tool in tools:
        for example in tool.examples:
            prompt += f"User: {example.input}\nAssistant: {example.output}\n"

    return prompt
