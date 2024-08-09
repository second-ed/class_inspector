import logging
import logging.config
import os
from pathlib import Path
from typing import Sequence, TypeVar, Union

from dotenv import load_dotenv

T = TypeVar("T")


def is_logging_enabled(src: str):
    if os.path.exists(_get_dir_path(__file__, 2, "envs/.env")):
        load_dotenv(_get_dir_path(__file__, 2, "envs/.env"))
        return os.getenv("ENABLE_LOGGING", "false").lower() == "true"
    return False


def setup_logger(file, idx) -> bool:
    logs_folder = _get_dir_path(file, idx, "logs")
    os.makedirs(logs_folder, exist_ok=True)
    logging.config.fileConfig(
        _get_dir_path(file, idx, "logging.ini"),
        defaults={"root": logs_folder},
    )
    return True


def compress_logging_value(item: T) -> Union[T, str]:
    if isinstance(item, (bool, int, float, str)):
        return item
    if isinstance(item, Sequence):
        if len(item) > 10:
            return f"len({len(item)})"
        return item
    return item


def _get_dir_path(src: str, idx: int, dst: str) -> str:
    curr_dir = Path(src).parents[idx]
    return str(curr_dir.joinpath(dst)).replace("\\", "/")
