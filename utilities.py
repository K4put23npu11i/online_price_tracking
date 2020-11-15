import logging
from datetime import datetime
import pandas as pd
import json
import os
import requests
import uuid


def create_new_id(id_type: str):
    prefix = ""
    if id_type.lower() in ["users", "user", "u", "u_"]:
        prefix = "u_"
    elif id_type.lower() in ["articles", "article", "a", "a_"]:
        prefix = "a_"
    else:
        logging.warning(f"Given id_type {id_type} is not specified")
    new_id = prefix + str(uuid.uuid4())
    return new_id


def write_file(base_path: str, filename: str, content: str):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    full_path = os.path.join(base_path, filename)
    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        logging.exception(e)
        raise e


def read_file(base_path: str, filename: str, file_type: str):
    try:
        full_path = os.path.join(base_path, filename)
        with open(full_path, 'r', encoding="utf-8") as openfile:
            if file_type.lower() == "json":
                file = json.loads(openfile.read())
            else:
                logging.error("Given file type ({file_type}) is not supported to read!")
            return file
    except BaseException as e:
        logging.exception(e)
        raise e


def check_if_file_exists_in_directory(path: str, filename: str) -> bool:
    try:
        all_files = os.listdir(path)
        if filename in all_files:
            return True
        else:
            return False
    except:
        return False


def read_csv_from_disc(path: str, filename: str) -> pd.DataFrame:
    if ".csv" not in filename:
        filename += ".csv"

    path = os.path.join(path, filename)
    df = pd.read_csv(path, index_col=0)
    return df


def write_dataframe_to_disc_as_csv(path: str, filename: str, content: pd.DataFrame):
    if ".csv" not in filename:
        filename += ".csv"
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, filename)
    content.to_csv(path)
