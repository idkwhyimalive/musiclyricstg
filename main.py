#!/usr/bin/python
# -*- coding: utf-8 -*-

# MusicLyricsBot - цей бот відправлятиме тобі текст пісні. "Виконавець назва пісні" з таким форматом буде знаходити бот текст пісні
# Libs: aiogram, bs4, requests, regex
# API: Genius
# 25.08.20 - початок створення, знову ж таки мені 15
# Парс працює на основі API Genius найбільшого сайту з наявністю текстів пісень (є не всі, дуже непопулярні артисти не будуть присутні). Є ще musixmatch, думав щодо нього, але я не пам'ятаю чи важко там з API
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from lyrics import lyrics
TGBot = ''
GENIUS_TOKEN = ''
bot = Bot(token=TGBot)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def start_message(message):
    bot.send_message(message.chat.id, """Приветствую. Я могу отправить вам текст песни которую вы мне напишете, если она будет в базе Genius, то я вам отправлю полностью текст песни. \nВ дальнейшем, я надеюсь, мой создатель добавит возможность брать текст песен и с других сайтов, но пока, что вот так

Одним сообщением напиши, на первом месте исполнитель, а на втором название трека, без ошибок главное. 
Примерно так: исполнитель название трека

Команды что доступны:
/start - начать работу
/creator - получить контакты создателя

p.s если я вам отправил \"None\" вместо текста, то знайте у меня бывают такие баги, просто снова отправьте исполнителя и название трека, и всё заработает""")

@dp.message_handler(commands=['creator'])
async def creator_message(message):
    bot.send_message(message.chat.id, "Телеграмм разработчика: @idkwhyimalive",disable_web_page_preview = True)

@dp.message_handler(content_types=['text'])
async def send_message(message):
    art = message.text.split(' ', 1)
    artist, title = art[0], art[1]
    song = lyrics(artist, title, GENIUS_TOKEN)
    bot.send_message(message.chat.id, "Вот тебе текст: \n\n" + song.extract_lyrics())

if __name__ == '__main__':
    executor.start_polling(dp)