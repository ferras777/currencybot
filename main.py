import os
import random
import re

import requests
import telebot
from bs4 import BeautifulSoup as Bs

# VARIABLES
NOT_AVAILABLE = 'недоступен, попробуйте через минуту.'
TOKEN = os.environ['TELEGRAM_TOKEN']
USDRUB = "https://www.tinkoff.ru/invest/currencies/USDRUB/pulse/"
EURRUB = "https://www.tinkoff.ru/invest/currencies/EURRUB/"
OILUSD = "https://quote.rbc.ru/ticker/181206"

bot = telebot.TeleBot(TOKEN)


# Add logs, add none except
# Gas price
@bot.message_handler(commands=['start'])
def euro_handler(message):
    bot.send_message(message.chat.id, 'Присылает актуальные курсы валют: /dollar, /euro')


@bot.message_handler(commands=['dollar'])
def dollar_handler(message):
    bot.send_message(message.chat.id, 'Курс доллара {0}'.format(get_currency(USDRUB)))


@bot.message_handler(commands=['euro'])
def euro_handler(message):
    bot.send_message(message.chat.id, 'Курс евро {0}'.format(get_currency(EURRUB)))


@bot.message_handler(commands=['oil'])
def oil_handler(message):
    bot.send_message(message.chat.id, 'Курс нефти {0}'.format(get_oil(OILUSD)))


@bot.message_handler(commands=['joke'])
def joke_handler(message):
    names = ["Антон", "Катя", "Таня", "Даня", "Илья"]
    jokes = ["{0} отправьте фотографии карточки со всех сторон, вы выиграли в лотерее 100000$, пришлём вам деньги"]
    bot.send_message(message.chat.id, random.choice(jokes).format(random.choice(names)))


@bot.message_handler(commands=['patchnotes'])
def patch_notes_handler(message):
    patch_note = '1. Фикс курса 2. Антон привет! 3. Добавлены патч ноты 4. Добавлена секретная функция 5. ' \
                 'Исправление, если нет ответа от сервера'
    bot.send_message(message.chat.id, patch_note)


def get_currency(url):
    r = requests.get(url)
    if r.status_code != 200:
        return NOT_AVAILABLE
    regex = re.compile('.*priceValue.*')
    soup = Bs(r.text, "html.parser")
    currency = soup.findAll("span", {"class": regex})
    for price in currency:
        search = re.search(r'[\d,]+', price.text)
        return search.group(0) + 'р.'


def get_oil(url):
    r = requests.get(url)
    if r.status_code != 200:
        return NOT_AVAILABLE
    soup = Bs(r.text, "html.parser")
    oil_price = soup.find("span", {"class": "chart__info__sum"})
    return oil_price.text


bot.polling()
