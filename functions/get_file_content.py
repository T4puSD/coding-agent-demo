from pathlib import Path
from utils.util import is_within_working_dir
from config.config import config


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs: Path = Path(working_directory).resolve()
        file: Path = (working_dir_abs / file_path).resolve()

        if not is_within_working_dir(working_dir_abs, file):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not file.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with file.open("r") as f:
            file_content = f.read(config.FILE_CONTENT_MAX_READ_SIZE)

            # if next 10 character read return data then it means
            # the file contains more data
            if f.read(10):
                file_content += f'[...File "{file_path}" truncated at {config.FILE_CONTENT_MAX_READ_SIZE} characters]'
            return file_content
    except Exception as e:
        return f"Error: Unable to read file content. Cause: {e}"
