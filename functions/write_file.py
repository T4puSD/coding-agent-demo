from pathlib import Path

from google.genai import types
from utils.util import is_within_working_dir, is_empty

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file content in the specified file_path, constrained to the working directory. This function will override content of file if writing to an existing file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to write file to, relative to the working directory. This is a required parameter.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file. This is a requried parameter.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = Path(working_directory).resolve()
        file = Path(abs_working_dir / file_path).resolve()

        if not is_within_working_dir(abs_working_dir, file):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if is_empty(content):
            return (
                f'Error: Cannot write to "{file_path}" as the content to write is empty'
            )

        sync_dirs(file)
        with file.open("w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Unable to write to "{file_path}". Cause: {e}'


def sync_dirs(file: Path):
    if not file.exists():
        parent_dir = file.parent
        if not parent_dir.exists():
            parent_dir.mkdir()
