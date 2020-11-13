import logging
from datetime import datetime
import pandas as pd
import json
import os
import requests

import utilities as utils


def add_article_to_shopping_list(articles: dict, art_link: str, user_id: str, price_limit: float):
    new_id = utils.create_new_id(id_type="article")
    articles[new_id] = {"article_name": new_id,
                        "article_link": art_link,
                        "shopping_platform": get_shopping_platform_by_link(art_link),
                        "price_limit": [{user_id: price_limit}]
                        }
    logging.debug(f"New article created with id: {new_id}")
    return articles


def delete_article_from_shopping_list(articles: dict, article_id: str):
    if article_id in articles.keys():
        del articles[article_id]
        logging.debug(f"Article with id {article_id} got deleted.")
    else:
        logging.error(f"Tried to delete Article with id {article_id}, but this id is not included in the dict!")
    return articles


def get_article_id_by_name(articles: dict, article_name: str):
    searched_article_id = None
    for current_article_id in articles:
        if articles[current_article_id]["article_name"] == article_name:
            searched_article_id = current_article_id
            break
    return searched_article_id


def edit_article_from_shopping_list(articles: dict, ):
    return None


def update_article_price_limit_for_single_user(articles: dict, ):
    return None


def update_article_price_limit_for_all_users(articles: dict, ):
    return None


def read_shopping_articles_from_file_to_json():
    path = os.getcwd()
    path = os.path.join(path, "data/")
    file = "shopping_articles.txt"
    raw_file = utils.read_file(base_path=path, filename=file, file_type="json")
    if type(raw_file) == dict:
        articles_json = raw_file
    else:
        articles_json = None
        logging.error(f"Read in file is type {type(raw_file)}!")
    return articles_json


def save_shopping_articles_from_json_to_file(articles: dict):
    path = os.getcwd()
    path = os.path.join(path, "data/")
    file = "shopping_articles.txt"
    content = json.dumps(articles, indent = 4)
    utils.write_file(base_path=path, filename=file, content=content)
    logging.debug("File successfully written to system.")
    return None


def get_shopping_platform_by_link(link: str) -> str:
    platform = ""
    if "amazon" in link:
        platform = "Amazon"

    return platform


def create_some_dummy_articles():
    articles = {}
    articles = add_article_to_shopping_list(articles=articles, art_link="https://www.amazon.de/dp/B084DWG2VQ",
                                            user_id="u_001", price_limit=50.0)
    articles = add_article_to_shopping_list(articles=articles, art_link="https://www.amazon.de/dp/B07Y9D3XX1",
                                            user_id="u_002", price_limit=15.0)
    return articles


if __name__ == "__main__":
    print("Hello")
    my_articles = create_some_dummy_articles()
    save_shopping_articles_from_json_to_file(my_articles)
    print("Done")
