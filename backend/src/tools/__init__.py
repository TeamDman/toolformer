from glob import glob
import os.path
import importlib
import traceback
from state import State
from tools.base import Tool
from typing import *

tools: List[Tool] = []

for path in glob("tools/*.py"):
    if path.endswith("__init__.py"):
        continue
    if path.endswith("base.py"):
        continue
    if path.endswith("helpers.py"):
        continue
    tool_name = os.path.basename(path)[:-3]
    module = importlib.import_module(f"tools.{tool_name}")
    tool_cls = getattr(module,f"{tool_name.capitalize()}Tool")
    tools.append(tool_cls())

tools_dict = {tool.name: tool for tool in tools}

print(f"[TOOLS] Found {len(tools)} tools: {', '.join([tool.name for tool in tools])}")



# returns (toolUsed, result)
async def handle_tool_invocation(state: State, response: str) -> Tuple[Literal[False], None] | Tuple[Literal[True],str]:
    # check for tool invocation and capture parameters
    try:
        import re
        pattern = r".*\[\s*(\w+)\((.*?)\)\s*->\s*"
        found = re.match(pattern, response, re.DOTALL)
        if found:
            tool_name = found.group(1)
            params = found.group(2)
            print(f"[TOOLS] found tool invocation: {tool_name}({params})")
            tool = tools_dict[tool_name]
            if tool:
                result = tool.method(state, params)
                return True, result
        else:
            print(f"[TOOLS] no tool invocation found")
            return False, None
    except Exception as e:
        print(f"[TOOLS] tool invocation error: {e}")
        traceback.print_exc()
        return True, f"ERROR: {e}"
    return False, None

async def predict_with_tools(state: State, prompt: str, predict: Callable[[str, str], str]) -> Tuple[str, Any]:
    first_prompt = build_preprompt() + prompt + build_postprompt()
    print(f"[TOOLS] predicting")
    first_response = await predict(first_prompt, "->")
    if "User:" in first_response:
        first_response, bad = first_response.split("User:", maxsplit=1)
        print("[TOOLS] bad: ", bad)
    if "\n" in first_response:
        first_response, bad = first_response.split("\n", maxsplit=1)
        print("[TOOLS] bad: ", bad)
        
    print(f"[TOOLS] first_response: \"{first_response}\"")
    
    tool_was_used, result = await handle_tool_invocation(state, first_response)
    if tool_was_used:
        assert result is not None
        second_prompt = first_prompt + first_response + result + "]"
        # second_response = await predict(second_prompt, None)
        second_response = await predict(second_prompt, "\n")
        full_response = first_response + result + "]" + second_response
        return full_response, {
            "first_prompt": first_prompt,
            "first_response": first_response,
            "second_prompt": second_prompt,
            "second_response": second_response,
        }
        
    else:
        return first_response, {
            "first_prompt": first_prompt,
            "first_response": first_response,
        }


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

    # prompt += (
    #     "\n"
    #     "You are not required to use tools to respond to the user."
    #     "\n"
    # )

    # list examples
    for tool in tools:
        for example in tool.examples:
            prompt += f"User: {example.input}\nAssistant: {example.output}\n"

    return prompt
