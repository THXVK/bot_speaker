import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
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
    bot.register_next_step_handler(msg, )


def text_to_speach(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    if text == '/stop':
        bot.send_message(chat_id, 'сессия прервана, чтобы продолжить, напишите /tts')
    elif text.startswith('/'):
        bot.send_message(chat_id, 'Если хотите использовать команды, напишите /stop')
    else:
        ...
