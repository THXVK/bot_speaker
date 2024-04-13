import telebot
from telebot.types import Message

from data import check_len, add_new_message
from config import TOKEN, MAX_LEN_PER_MESSAGE, MAX_SIMBOLS
from log import logger

bot = telebot.TeleBot(token=TOKEN)


# region commands
@bot.message_handler(commands=['tts'])
def tts(message: Message):
    message_register(message.chat.id)


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет! Я могу озвучить все, что ты напишешь')
    message_register(chat_id)
# endregion


def message_register(chat_id):
    msg = bot.send_message(chat_id, 'Что мне озвучить?')
    bot.register_next_step_handler(msg, message_processing)


def message_processing(message: Message):
    chat_id = message.chat.id
    text = message.text
    if text == '/stop':
        bot.send_message(chat_id, 'сессия прервана, чтобы продолжить, напишите /tts')
    elif text.startswith('/'):
        bot.send_message(chat_id, 'Если хотите использовать команды, напишите /stop')
    else:
        if len(text) > MAX_LEN_PER_MESSAGE:
            msg = bot.send_message(chat_id, 'ваше сообщение слишком длинное, напишите новое')
            bot.register_next_step_handler(msg, message_register)
        elif len(text) + check_len() >= MAX_SIMBOLS:
            bot.send_message(chat_id, 'общий лимит символов исчерпан')
        else:
            text_to_speach(message)


def text_to_speach(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    result = add_new_message(text, user_id)
    if result[0]:
        bot.send_voice(chat_id, result[1])
    else:
        bot.send_message(chat_id, result[1])