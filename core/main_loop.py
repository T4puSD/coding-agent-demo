from google.genai import types
from functions.call_function import call_function

def run_main_loop(client, messages, available_functions, system_prompt, is_verbose, max_iterations=20):
    """Run the main conversation loop with the Gemini API."""
    iteration = max_iterations

    while iteration > 0:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )

            if is_verbose and response.usage_metadata:
                print("\n\n")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    if candidate and candidate.content:
                        messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, is_verbose)

                    if not function_call_result or not function_call_result.parts:
                        raise Exception(f"No response from function calling {function_call_part.name}")

                    function_response = function_call_result.parts[0].function_response.response
                    function_response_text = str(function_response)

                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part(text=function_response_text)],
                        )
                    )

                    if is_verbose:
                        print(f"-> {function_response}")
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

        iteration -= 1

    if iteration == 0:
        print("Error: unable to produce answer with max iteration")
