from pathlib import Path


def is_within_working_dir(working_dir_abs: Path, dir_abs: Path):
    return dir_abs.as_posix().startswith(working_dir_abs.as_posix())


def is_empty(content: str):
    return not content or content is None or content == ""
