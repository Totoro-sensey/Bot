import requests
from aiogram import types
# from bs4 import BeautifulSoup

from loader import dp, bot

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

url = "https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?q="


@dp.message_handler(content_types=['text'])
async def get_message(message: types.Message):
    url = "https://www.dns-shop.ru/search?q=" + message.text
    request = requests.get(url)
    # soup = BeautifulSoup(url, "html.parser")

    # all_links = soup.find_all("a")
    # for link in all_links:
    #     print(link["href"])
    #     url = "https://www.golden-swim.by/" + link["href"]
    #     request = requests.get(url)
    #     soup = BeautifulSoup(request.text, "html.parser")
    #
    #     name = soup.find("h1", class_="product__title heading").text
    #     price = soup.find("span", class_="product__price-cur").text
    #     img = soup.find("img", class_="lazyload entered loaded")
    #
    #     await bot.send_photo(message.chat.id, img,
    #                          caption="<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
    #                          parse_mode="html"
    #                          )
