from sys import argv

from config.config import config
from google import genai
from google.genai import types

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

# prepare user prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# create generation request to geminmi flash api
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

# output
print(response.text)
if is_verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
