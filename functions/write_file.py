from pathlib import Path
from utils.util import is_within_working_dir, is_empty


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
