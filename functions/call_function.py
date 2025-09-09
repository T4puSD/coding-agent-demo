from google.genai import types
from google.genai.types import Content, FunctionCall
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from utils.util import is_empty
from config.config import config

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part: FunctionCall, verbose=False) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(
            f" - Calling function: {function_call_part.name}{f'({function_call_part.args})' if verbose else ''}"
        )

    function_name = function_call_part.name or ""
    if is_empty(function_name):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": "Error: function name can not be empty"},
                )
            ],
        )

    function = functions[function_name]
    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    kwrgs = function_call_part.args
    kwrgs["working_directory"] = config.AI_AGENT_WORKING_DIRECTORY
    function_result = function(**kwrgs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
