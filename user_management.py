import logging
from datetime import datetime
import pandas as pd
import json
import os
import requests

import utilities as utils


def ask_user_for_user_information():
    print("Hey there, let's create a new User!")
    mes_name = "\nTell me the name of the new User?\n"
    print(mes_name)
    name = "Dummy"

    mes_mail = "\nTell me the mail adress for notifications:\n"
    print(mes_mail)
    mail = "Dummy_mail"

    mes_note = "\nDoes the User want to recieve regular emails about the products? (y/n)\n"
    print(mes_note)
    overview_note = "y"

    return name, mail, overview_note


def create_and_add_new_user(existing_users: pd.DataFrame):
    new_id = utils.create_new_id(id_type="users")
    name, mail, overview_note = ask_user_for_user_information()
    new_user = pd.DataFrame(columns=["user_id", "name", "mail", "overview_note", "creation_date", "last_updated"])
    now = str(datetime.now())
    row = {"user_id": new_id, "name": name, "mail": mail, "overview_note": overview_note,
           "creation_date": now, "last_updated": now}

    new_user = new_user.append(row, ignore_index=True)

    if existing_users is None:
        updated_users = new_user
    else:
        updated_users = pd.concat([existing_users, new_user]).reset_index(drop=True)

    #    logging.debug(f"New user created with id: {new_id}")
    save_users_to_disc(users=updated_users)
    return users


def delete_user_by_id(users: pd.DataFrame, user_id: str):
    all_user_ids = list(users["user_id"])

    if user_id not in all_user_ids:
        print("User ID not in users")
        return None

    matching_index = all_user_ids.index(user_id)

    users = users.drop(index=matching_index).reset_index(drop=True)
    save_users_to_disc(users=users)

    return users


def get_user_id_by_name(users: pd.DataFrame, name: str):
    all_names = list(users["name"])

    if name not in all_names:
        print("Name not in users!")
        return None

    matching_index = all_names.index(name)

    user_id = users.iloc[matching_index]["user_id"]

    return user_id


def edit_user_by_id(users: pd.DataFrame, user_id: str):
    all_user_ids = list(users["user_id"])

    if user_id not in all_user_ids:
        print("User ID not in users")
        return None

    matching_index = all_user_ids.index(user_id)

    change_labels = ["name", "mail", "overview_note"]
    something_changed = False

    for label in change_labels:
        current_value = users.iloc[matching_index][label]
        print(f"Current value: {current_value}")
        change_it = input("Change it?")
        if change_it == "y":
            something_changed = True
            new_value = input("new value:")
            users.iloc[matching_index][label] = new_value

    if something_changed is True:
        print("Values updated. Save new values")
        users.iloc[matching_index]["last_updated"] = str(datetime.now())

        save_users_to_disc(users=users)

    return users


def load_users_from_disc():
    path = "data"
    file = "scraping_users.csv"
    file_exists = utils.check_if_file_exists_in_directory(path=path, filename=file)
    print(f"File exists?: {file_exists}")
    if file_exists is True:
        users = utils.read_csv_from_disc(path=path, filename=file)
        print("Load from disc")
    else:
        print("Create new user")
        users = create_and_add_new_user(existing_users=None)

    return users


def save_users_to_disc(users: pd.DataFrame):
    path = "data"
    file = "scraping_users.csv"
    utils.write_dataframe_to_disc_as_csv(path=path, filename=file, content=users)
    return None


def testing(users):
    users = create_and_add_new_user(existing_users=users)
    print(users)
    user_id = get_user_id_by_name(users=users, name="Dummy")
    print(user_id)
    users = edit_user_by_id(users=users, user_id=user_id)
    print(users)
    users = delete_user_by_id(users=users, user_id=user_id)
    print(users)
    return None


if __name__ == "__main__":
    users = load_users_from_disc()
    print(users)
#    testing(users=users)