import sys
from pathlib import Path
from subprocess import run
from utils.util import is_within_working_dir


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

        if not result.stdout:
            return "No output produced."

        response = f"STDOUT: \n{result.stdout} \nSTDERR: \n{result.stderr}"

        if result.returncode != 0:
            response += f"\n Process exited with code {result.returncode}"

        return response

    except Exception as e:
        return f"Error: executing Python file: {e}"
