from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from smile import get_anekdot


def get_main_keyboard():
    reply_keyboard = [['Анекдот']]
    main_keyboard = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    return main_keyboard


def start(update, context):
    update.message.reply_text('Выбирай!', reply_markup=get_main_keyboard())


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anekdot))
    updater.start_polling()
    updater.idle()

