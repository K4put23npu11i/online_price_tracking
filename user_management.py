import logging
from datetime import datetime
import pandas as pd
import json
import os
import requests

import utilities as utils


def create_new_user(users: dict, name: str, mail: str, article_note: bool, overview_note: bool):
    new_id = utils.create_new_id(users, "users")
    users[new_id] = {"name": name,
                     "mail": mail,
                     "article_notification": article_note,
                     "overview_notification": overview_note
                     }
    logging.debug(f"New user created with id: {new_id}")
    return users


def delete_user_by_id(users: dict, user_id: str):
    if user_id in users.keys():
        del users[user_id]
        logging.debug(f"User with id {user_id} got deleted.")
    else:
        logging.error(f"Tried to delete user with id {user_id}, but this id is not included in the users dict!")
    return users


def get_user_id_by_name(users: dict, user_name: str):
    searched_user_id = None
    for current_user_id in users:
        if users[current_user_id]["name"] == user_name:
            searched_user_id = current_user_id
            break
    return searched_user_id


def edit_user(users: dict, user_id: str, change_key: str, new_change_value: str):
    if user_id in users.keys():
        if change_key in users[user_id].keys():
            users[user_id][change_key] = new_change_value
            logging.debug(f"User updated. Key: {change_key} is not {new_change_value} for user with id {user_id}")
            return users
        else:
            logging.error(f"Given key {change_key} is not in keys of a user!")
            return None
    else:
        logging.error(f"Given user_id {user_id} is not in users!")
        return None


def save_users_from_json_to_file(users: dict):
    path = os.getcwd()
    path = os.path.join(path, "data/")
    file = "users.txt"
    content = json.dumps(users, indent = 4)
    utils.write_file(base_path=path, filename=file, content=content)
    logging.debug("File successfully written to system.")


def read_users_from_file_to_json():
    path = os.getcwd()
    path = os.path.join(path, "data/")
    file = "users.txt"
    raw_file = utils.read_file(base_path = path, filename=file, file_type="json")
    if type(raw_file) == dict:
        users_json = raw_file
    else:
        users_json = None
        logging.error(f"Read in file is type {type(raw_file)}!")
    return users_json


def create_some_dummy_users():
    users = {}
    users = create_new_user(users=users, name="Name1", mail="Mail1", article_note=True, overview_note=True)
    users = create_new_user(users=users, name="Name2", mail="Mail2", article_note=False, overview_note=True)
    users = create_new_user(users=users, name="Name3", mail="Mail3", article_note=True, overview_note=False)
    users = create_new_user(users=users, name="Name4", mail="Mail4", article_note=False, overview_note=False)
    return users


if __name__ == "__main__":
    print("Hello")
    my_users = create_some_dummy_users()
    save_users_from_json_to_file(my_users)
    print("Done")

