import logging
import logging.config
import os
from pathlib import Path
from typing import Sequence, TypeVar

import pandas as pd
from openpyxl import Workbook

T = TypeVar("T")


def setup_logger(file, idx) -> bool:
    logs_folder = get_dir_path(file, idx, "logs")
    os.makedirs(logs_folder, exist_ok=True)
    logging.config.fileConfig(
        get_dir_path(file, idx, "logging.ini"),
        defaults={"root": logs_folder},
    )
    return True


def compress_logging_value(item: T) -> T:
    if isinstance(item, (bool, int, float, str)):
        return item
    if isinstance(item, Sequence):
        if len(item) > 10:
            return f"len({len(item)})"
        return item
    if isinstance(item, pd.DataFrame):
        return item.info()
    if isinstance(item, Workbook):
        return item.sheetnames
    return item


def get_dir_path(src: str, idx: int, dst: str) -> str:
    curr_dir = Path(src).parents[idx]
    return str(curr_dir.joinpath(dst)).replace("\\", "/")
