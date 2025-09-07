from pathlib import Path
from utils.util import is_within_working_dir


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = Path(working_directory).resolve()
        dir_abs = Path(working_dir_abs / directory).resolve()

        if not is_within_working_dir(working_dir_abs, dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not dir_abs.is_dir():
            return f'Error: "{directory}" is not a directory'

        return "\n".join(_list_dirs(dir_abs))
    except Exception as e:
        return f"Error: Failed to get files info. Cause: {e}"


def _list_dirs(dir_abs: Path):
    files_info = []
    for item in dir_abs.iterdir():
        files_info.append(
            f"- {item.name}: file_size={item.stat().st_size} bytes, is_dir={item.is_dir()}"
        )
    return files_info
