import requests
from bs4 import BeautifulSoup


def get_bash(bot, update):
    res = requests.get("https://bash.im/forweb/?u")
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.text
    data = data[136:-82]
    bot.message.reply_text(data)


def get_anekdot(bot, update):
    res = requests.get('http://anekdotme.ru/random')
    soup = BeautifulSoup(res.text, 'html.parser')
    find = soup.select('.anekdot_text')
    for text in find:
        soup = (text.getText().strip())
    bot.message.reply_text(soup)
