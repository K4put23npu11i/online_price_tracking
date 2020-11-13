from requests_html import HTMLSession
import nest_asyncio

nest_asyncio.apply()

asins = ["B084DWG2VQ"]

s = HTMLSession()

for asin in asins:

    url = "https://www.amazon.de/dp/" + asin
    print(url)

    r = s.get(url=url)

    r.html.render(sleep=1)

    price = r.html.find("#priceblock_ourprice")[0].text

    print(price)

    title = r.html.find("#productTitle")[0].text

    print(title)