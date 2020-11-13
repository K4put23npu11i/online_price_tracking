import logging
from datetime import datetime
import pandas as pd
import json
import os
import requests

import user_management as user_mngmt
import article_management as art_mngmt
import utilities as utils
import price_scraping as scrap

# Configure Logging
logger = logging.getLogger()
# create file handler which logs even debug messages
fh = logging.FileHandler(str(__file__.split('/')[-1].split('.')[0]) + '.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s [%(funcName)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

# Measure running time:
start_time = datetime.now()
logger.info('Script started successfully!')


def scrape_all_articles(arts: dict):
    amazon_asins = []
    for art_id in arts:
        article = arts[art_id]
        if article["shopping_platform"] == "Amazon":
            amazon_asins.append(article["article_link"].split("/")[-1])

    new_scraping_data = scrap.scraping_for_amazon_asins(asins=amazon_asins)

    file_exists = utils.check_if_file_exists_in_directory(path="data", filename="scraping_history.csv")

    if file_exists is True:
        scraping_data = utils.read_csv_from_disc(path="data", filename="scraping_history.csv")
        updated_data = pd.concat([scraping_data, new_scraping_data]).reset_index(drop=True)
        utils.write_dataframe_to_disc_as_csv(path="data", filename="scraping_history.csv", content=updated_data)

    else:
        utils.write_dataframe_to_disc_as_csv(path="data", filename="scraping_history.csv", content=new_scraping_data)

    return None


def main():
    users = user_mngmt.read_users_from_file_to_json()
    articles = art_mngmt.read_shopping_articles_from_file_to_json()

    scrape_all_articles(arts=articles)

    return None


if __name__ == "__main__":
    main()

# Measure running time:
end_time = datetime.now()
logger.info('End of Script!')
logger.debug('Runtime of script: {}'.format(end_time - start_time))