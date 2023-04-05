import telebot
import requests
import time
import config # создаёте config.py туда записываете свой токен token = ""
from bs4 import BeautifulSoup

channel_id = "" #ссылка на ТГ-канал, начинающийся на @
bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == "/start":
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(channel_id, post_text[0])
                time.sleep(1800)
    else:
        bot.send_message(message.from_user.id, "Я Вас не понимаю. Напишите Старт")


def parser(back_post_id):
    URL = "https://habr.com/ru/search/?target_type=posts&q=python&order_by=date" #ссылка с хабра, откуда хотите парсить

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("article", id=True)
    post_id = post["id"]

    if post_id != back_post_id:
        post_title = soup.find("a", class_="tm-title__link").text.strip()

        post_url = soup.find("a", class_="tm-title__link", href=True)["href"].strip()
        post_url = "https://habr.com" + post_url
        page = requests.get(post_url)
        soup = BeautifulSoup(page.content, "html.parser")
        post_description = soup.find("p").text.strip()

        return f"{post_title}\n\n{post_description}\n\n{post_url}", post_id
    else:
        return None, post_id


bot.polling()