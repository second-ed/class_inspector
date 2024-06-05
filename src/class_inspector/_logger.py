import logging
import logging.config
import os
from pathlib import Path


def setup_logger(file, idx) -> bool:
    logs_folder = get_dir_path(file, idx, "logs")
    os.makedirs(logs_folder, exist_ok=True)
    logging.config.fileConfig(
        get_dir_path(file, idx, "logging.ini"),
        defaults={"root": logs_folder},
    )
    return True


def get_dir_path(src: str, idx: int, dst: str) -> str:
    curr_dir = Path(src).parents[idx]
    return str(curr_dir.joinpath(dst)).replace("\\", "/")
