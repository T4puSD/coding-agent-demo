import sys

def parse_arguments():
    """Parse command line arguments and return user prompt and verbose flag."""
    if len(sys.argv) < 2 or sys.argv[1] is None or sys.argv[1] == "":
        print("Please provide a prompt as argument")
        sys.exit(1)

    is_verbose = "--verbose" in sys.argv
    user_prompt = sys.argv[1]

    return user_prompt, is_verbose
