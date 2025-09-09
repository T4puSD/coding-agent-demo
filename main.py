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

# create generation request to geminmi flash api
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

# output

if response.function_calls:
    for function_call_part in response.function_calls:
        function_call_result: types.Content = call_function(
            function_call_part, is_verbose
        )

        if not function_call_result.parts[0].function_response.response:
            raise Exception(
                f"No response got from function calling {function_call_part.name}"
            )

        if is_verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

else:
    print(response.text)

if is_verbose:
    print("\n\n")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
