import requests
from bs4 import BeautifulSoup


def get_anekdot(bot, update):
    res = requests.get('http://anekdotme.ru/random')
    soup = BeautifulSoup(res.text, 'html.parser')
    find = soup.select('.anekdot_text')
    for text in find:
        soup = (text.getText().strip())
    bot.message.reply_text(soup)
