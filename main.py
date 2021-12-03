from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
from smile import get_anekdot, get_bash
from weather import get_city_id, request_current_weather, request_forecast
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_main_keyboard():
    reply_keyboard = [['Цитата BasOrg'], ['Анекдот'], ['Погода']]
    main_keyboard = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    return main_keyboard


def start(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отправил start.', user.first_name)
    update.message.reply_text('Выбирай!', reply_markup=get_main_keyboard())


def weather(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отправил Погода.', user.first_name)
    update.message.reply_text('Введи название города', reply_markup=ReplyKeyboardRemove())
    return GET_CITY


def get_city(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отправил город.', user.first_name)
    city = update.message.text
    try:
        city_id = get_city_id(city)
        context.user_data['city_id'] = city_id
        reply_keyboard = [['Сейчас'], ['Прогноз'], ['Назад']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Пожалуйста, выберите:', reply_markup=markup_key)
    except Exception as e:
        user = update.message.from_user
        logger.info('Пользователь %s отправил неправильный запрос.', user.first_name)
        update.message.reply_text(f'Нет города в базе', reply_markup=get_main_keyboard())
        print('Exception (find):', e)
        return -1
    return SEND


def send_weather_now(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отправил запрос погода сейчас.', user.first_name)
    dict_ = request_current_weather(context.user_data['city_id'])
    update.message.reply_text(dict_['Сейчас'], reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Выбирай!', reply_markup=get_main_keyboard())
    return ConversationHandler.END


def send_weather_forecast(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отправил запрос прогноза погоды.', user.first_name)
    text = ''
    dict_ = request_forecast(context.user_data['city_id'])
    for k, v in dict_.items():
        text += k + ' ' + v + '\n'
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Выбирай!', reply_markup=get_main_keyboard())
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info('Пользователь %s отменил действие.', user.first_name)
    update.message.reply_text('Выбирай!', reply_markup=get_main_keyboard())
    return -1


SEND, GET_CITY = 0, 1


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Цитата BasOrg'), get_bash))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anekdot))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Погода'), weather)],
        states={
            SEND: [MessageHandler(Filters.regex('Сейчас'), send_weather_now),
                   MessageHandler(Filters.regex('Прогноз'), send_weather_forecast)],
            GET_CITY: [MessageHandler(Filters.text, get_city)]},
        fallbacks=[CommandHandler('start', start), MessageHandler(Filters.regex('Назад'), cancel)],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
