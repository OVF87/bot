from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
from config import TOKEN

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
    updater.start_polling()
    updater.idle()

