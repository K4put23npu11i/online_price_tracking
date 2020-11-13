from requests_html import HTMLSession
import nest_asyncio
import pandas as pd
from datetime import datetime


def scraping_for_amazon_asins(asins: list) -> pd.DataFrame:
    columns = ["timestamp", "asin", "price", "title"]
    scraped_articles = pd.DataFrame(columns=columns)

    s = HTMLSession()

    for asin in asins:
        url = "https://www.amazon.de/dp/" + asin
        print(url)

        r = s.get(url=url)
        r.html.render(sleep=2)

        price = r.html.find("#priceblock_ourprice")[0].text
        print(price)

        title = r.html.find("#productTitle")[0].text
        print(title)

        # create new row and append to the dataframe
        new_row = {"timestamp": str(datetime.now()), "asin": asin, "price": price, "title": title}
        scraped_articles = scraped_articles.append(new_row, ignore_index=True)

    s.close()

    return scraped_articles


def test_scraping():
    asins = ["B084DWG2VQ"]
    arts = scraping_for_amazon_asins(asins=asins)
    print(arts)
    return None


if __name__ == "__main__":
    test_scraping()
