import math

import telebot
from telebot.types import Message

from speaking import make_requests, speech_to_text
from data import check_len, add_new_message, check_len_for_user, check_stt_block_num, check_all_stt_blocks_num
from config import TOKEN, MAX_LEN_PER_MESSAGE, MAX_SIMBOLS, MAX_SIMBOLS_PER_USER, MAX_STT_BLOCK_PER_USER, \
    ALL_STT_BLOCKS_LIMIT

bot = telebot.TeleBot(token=TOKEN)


# region commands
@bot.message_handler(comands=['help'])
def help_message(message):
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


@bot.message_handler(commands=['stt'])
def stt(message: Message):
    voice_register(message.chat.id)


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Привет! Я могу озвучить все, что ты напишешь, для этого пропиши команду /tts. '
                     'Или /stt для перевода гс в текст')
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
    if message.text:
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
            elif check_len_for_user(chat_id) + len(text) > MAX_SIMBOLS_PER_USER:
                bot.send_message(chat_id, 'ваш лимит символов исчерпан, вы не можете озвучивать текст')
            else:
                text_to_speach(message)
    else:
        bot.send_message(chat_id, 'отправьте текстовое сообщение')


def text_to_speach(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    add_new_message(text, user_id, len(text), 0)
    result = make_requests(text)
    if result[0]:
        bot.send_voice(chat_id, result[1])
        message_register(chat_id)
    else:
        bot.send_message(chat_id, result[1])
# endregion
# region stt


def voice_register(chat_id):
    msg = bot.send_message(chat_id, 'Что мне распознать?')
    bot.register_next_step_handler(msg, voice_processing)


def voice_processing(message):
    user_id = message.from_user.id
    if not message.voice:
        if message.text:
            text = message.text
            if text == '/stop':
                bot.send_message(user_id, 'сессия прервана, чтобы продолжить, напишите /stt')
            elif text.startswith('/'):
                bot.send_message(user_id, 'Если хотите использовать команды, напишите /stop')
                voice_register(user_id)
            else:
                bot.send_message(user_id, 'вы должны отправить гс, а не текст')
                voice_register(user_id)
        else:
            bot.send_message(user_id, 'отправьте гс, а не файл')
        return
    else:
        dur = message.voice.duration
        if dur == 0:
            dur = 1

        if dur > 30:
            bot.send_message(user_id, 'гс слишком длинное')
            voice_register(user_id)
        else:
            blocks_duration = math.ceil(dur / 15)
            blocks = check_stt_block_num(user_id)

            if blocks + blocks_duration > MAX_STT_BLOCK_PER_USER:
                bot.send_message(user_id, 'ваш лимит на распознавание исчерпан')
            elif check_all_stt_blocks_num() + blocks_duration > ALL_STT_BLOCKS_LIMIT:
                bot.send_message(user_id, 'извините, общий лимит на распознавание исчерпан')
            else:
                speach_to_text(message, blocks_duration)


def speach_to_text(message, duration):

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)

    user_id = message.from_user.id
    chat_id = message.chat.id

    result = speech_to_text(file)
    text = result[1]
    if result[0]:
        add_new_message(text, user_id, 0, duration)
        bot.send_message(chat_id, result[1])
        voice_register(chat_id)
    else:
        bot.send_message(chat_id, result[1])


bot.infinity_polling()
