"""module level description"""

import re
from typing import Dict

import pandas as pd


def main(filepath: str) -> bool:
    data = read_data(filepath)
    data = clean_data(data)
    data_dict = _transform_data(data)

    for key, value in data_dict.items():
        data_dict[key] = rename_data(value)

    merged_data = merge_data(data_dict)

    return save_data(merged_data, filepath)


# this is a comment related to the function below
def read_data(filepath: str):
    if check_extension(filepath):
        return pd.DataFrame({})
    raise FileNotFoundError


def check_extension(filepath: str) -> bool:
    """this is a docstring

    Args:
        filepath (str): the filepath to check

    Returns:
        bool: if the extension is valid
    """
    return bool(filepath)


def clean_data(data):
    return data


def _transform_data(data) -> dict:
    def transform() -> dict:
        return {"data": data}

    return transform()


def rename_data(value) -> str:
    def replacer(match) -> str:
        content = match.group(1)
        cleaned_content = " ".join(content.split())
        return f"({cleaned_content})"

    return re.sub(r"\((.*?)\)", replacer, str(value.iloc[0, 0]), flags=re.DOTALL)


def merge_data(data_dict: Dict):
    # this is an inline comment that hopefully will stay
    data = pd.concat([v for v in data_dict.values()])
    return data


def save_data(data, filepath: str) -> bool:
    if filepath_exists(filepath):
        return True
    return False


def filepath_exists(filepath: str) -> bool:
    return bool(filepath)
