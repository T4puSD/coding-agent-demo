import sys
from pathlib import Path
from subprocess import run

from google.genai import types
from utils.util import is_within_working_dir

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python script located in the specified file_path with passed args parameters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of the python file, relative to the working directory. This is a required parameter.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The additional list of string arguments to pass while running the python file. This is an optional value and by default it is empty.",
                items=types.Schema(
                    type=types.Type.STRING, description="A single string argument"
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir: Path = Path(working_directory).resolve()
        file: Path = Path(abs_working_dir / file_path).resolve()

        if not is_within_working_dir(abs_working_dir, file):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file.exists():
            return f'Error: File "{file_path}" not found.'

        if not file.name.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = [sys.executable, file]
        if args:
            cmd = cmd + args

        result = run(
            cmd,  # command to run
            cwd=abs_working_dir,  # setting the working directory
            capture_output=True,  # capout subprocess stdout and stderr
            text=True,  # decode output to text
            check=True,  # reaise exception if fail
            timeout=30,  # timeout of 30 sec
        )

        if not result.stdout and not result.stderr:
            return "No output produced."

        response = ""
        if not result.stdout and result.stderr:
            response += f"STDERR: \n{result.stderr}"
        else:
            response += f"STDOUT: \n{result.stdout} \nSTDERR: \n{result.stderr}"

        if result.returncode != 0:
            response += f"\n Process exited with code {result.returncode}"

        return response

    except Exception as e:
        return f"Error: executing Python file: {e}"
