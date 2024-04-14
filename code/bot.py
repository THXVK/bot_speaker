import telebot
from telebot.types import Message

from speaking import make_requests
from data import check_len, add_new_message
from config import TOKEN, MAX_LEN_PER_MESSAGE, MAX_SIMBOLS


bot = telebot.TeleBot(token=TOKEN)


# region commands
@bot.message_handler(comands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     """
/start - начало диалога
/help - список команд
/stop - останавливает сессию
/tts - запускает сессию
                     """
                     )


@bot.message_handler(commands=['tts'])
def tts(message: Message):
    message_register(message.chat.id)


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет! Я могу озвучить все, что ты напишешь')
    message_register(chat_id)
# endregion


@bot.message_handler(content_types=['text'])
def echo(message: Message) -> None:
    """Функция ответа на некорректное сообщение от пользователя

    Функция отправляет сообщение с некорректным ответом от пользователя в формате
    'Вы напечатали: *сообщение пользователя*.что?'
    :param message: некорректное сообщение пользователя"""
    bot.send_message(chat_id=message.chat.id, text=f'Вы напечатали: {message.text}. Что?')


# region tts
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
        message_register(chat_id)
    else:
        if len(text) > MAX_LEN_PER_MESSAGE:
            bot.send_message(chat_id, 'ваше сообщение слишком длинное, напишите новое')
            message_register(chat_id)
        elif len(text) + check_len() >= MAX_SIMBOLS:
            bot.send_message(chat_id, 'общий лимит символов исчерпан, сейчас вы не можете озвучивать текст')
        else:
            text_to_speach(message)


def text_to_speach(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    add_new_message(text, user_id)
    result = make_requests(text)
    if result[0]:
        bot.send_voice(chat_id, result[1])
        message_register(chat_id)
    else:
        bot.send_message(chat_id, result[1])
# endregion


bot.infinity_polling()