from sys import argv

from config.config import config
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

# input arg validation
if len(argv) < 2 or argv[1] is None or argv[1] == "":
    print("Please provide a prompt as argument")
    exit(1)

# input
is_verbose = "--verbose" in argv
user_prompt = argv[1]

if is_verbose:
    print(f"User prompt: {user_prompt}\n")

# get client object
api_key = config.GEMINI_API_KEY
client = genai.Client(api_key=api_key)

# system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan without asking any question for clarification. You can perform the following operations:

- List files and directories
- Read contents of file
- Write new file or override existing file content
- Execute python file with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# prepare user prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

max_iteration = 20
while max_iteration > 0:
    if max_iteration == 0:
        print("Error: unable to produce answer with max iteration")
        break

    try:
        # create generation request to geminmi flash api
        response: types.GenerateContentResponse = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if is_verbose and response.usage_metadata:
            print("\n\n")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # output
        if response.candidates:
            for candidate in response.candidates:
                if candidate and candidate.content:
                    messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result: types.Content = call_function(
                    function_call_part, is_verbose
                )

                if (
                    not function_call_result
                    or not function_call_result.parts
                    or not function_call_result.parts[0]
                    or not function_call_result.parts[0].function_response
                    or not function_call_result.parts[0].function_response.response
                ):
                    raise Exception(
                        f"No response got from function calling {function_call_part.name}"
                    )

                function_response = function_call_result.parts[
                    0
                ].function_response.response
                function_response_text = str(function_response)

                messages.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=function_response_text)],
                    )
                )

                if is_verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
        else:
            if response.text:
                print(response.text)
            else:
                print("Error: no response from model")
            break
    except Exception as e:
        messages.append(
            types.Content(role="user", parts=[types.Part(text=f"Error: {e}")])
        )
    max_iteration -= 1
