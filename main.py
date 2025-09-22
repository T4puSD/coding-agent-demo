from google.genai import types

from core.argument_parser import parse_arguments
from core.client_manager import create_client
from core.prompt_manager import get_system_prompt
from core.main_loop import run_main_loop

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

# Parse arguments
user_prompt, is_verbose = parse_arguments()

if is_verbose:
    print(f"User prompt: {user_prompt}\n")

# Create client
client = create_client()

# Get system prompt
system_prompt = get_system_prompt()

# Prepare user prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

# Run main loop
run_main_loop(client, messages, available_functions, system_prompt, is_verbose)
