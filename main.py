import os
import re

import requests
import telebot
from bs4 import BeautifulSoup as Bs

# VARIABLES
TOKEN = os.environ['TELEGRAM_TOKEN']
USDRUB = "https://www.tinkoff.ru/invest/currencies/USDRUB/pulse/"
EURRUB = "https://www.tinkoff.ru/invest/currencies/EURRUB/"
OILUSD = "https://quote.rbc.ru/ticker/181206"

bot = telebot.TeleBot(TOKEN)


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


def get_currency(url):
    r = requests.get(url)
    regex = re.compile('.*priceValue.*')
    soup = Bs(r.text, "html.parser")
    currency = soup.findAll("span", {"class": regex})
    for price in currency:
        return price.text


def get_oil(url):
    r = requests.get(url)
    soup = Bs(r.text, "html.parser")
    oil_price = soup.find("span", {"class": "chart__info__sum"})
    return oil_price.text


bot.polling()
