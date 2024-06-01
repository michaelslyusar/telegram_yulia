# -*- coding: utf-8 -*-
import types
import json
import telebot
from dotenv import load_dotenv
import os
import sqlite3
from telebot import types
import random

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment PRIMARY KEY, user_id varchar(50), last_tarot_read date)')
    conn.commit()
    cur.close()
    conn.close()

    file = open('img/slide2.jpg', 'rb')
    bot.send_photo(message.chat.id, file)

    markup = types.InlineKeyboardMarkup()
    btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
    btn_horoscope = types.InlineKeyboardButton('Прогноз по гороскопу', callback_data='Zodiac')
    btn_affirmation = types.InlineKeyboardButton('Аффирмация дня', callback_data='Affirmation')

    markup.row(btn_tarot)
    markup.row(btn_horoscope, btn_affirmation)

    text = """Мудрый маг предлагает вам выбрать путь:

Откройте карту дня и узнайте, что ждёт вас впереди🔮 /card

загляните в звёзды и получите прогноз по вашему гороскопу
💫 /zodiac

или напитайте свой дух аффирмацией дня 💗 /affirmation

Каждый выбор откроет вам новый источник мудрости и вдохновения. Какой путь вы предпочтёте сегодня?"""
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['card'])
def card(message):
    text = 'Выбор сделан... Карта дня откроет вам завесу будущего и покажет, какие энергии и события ждут вас сегодня. Позвольте магу раскрыть перед вами тайны этого дня и получить важное предсказание.'

    file = open('./img/slide3.jpg', 'rb')
    bot.send_photo(message.chat.id, file)


    btn = types.InlineKeyboardButton('выбрать', callback_data='CardReveal')
    markup = types.InlineKeyboardMarkup()
    markup.add(btn)
    bot.send_message(message.chat.id, text,reply_markup=markup)

@bot.message_handler(commands=['zodiac'])
def zodiac(message):
    text = 'Выбор сделан... Звезды готовы рассказать вам о том, что они приготовили для вас. Прогноз по гороскопу откроет вам небесные секреты и поможет лучше понять, как использовать их в свою пользу.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['affirmation'])
def affirmation(message):
    text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии.'
    bot.send_message(message.chat.id,text)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'Card':
        text = 'Выбор сделан... Карта дня откроет вам завесу будущего и покажет, какие энергии и события ждут вас сегодня. Позвольте магу раскрыть перед вами тайны этого дня и получить важное предсказание.'

        file = open('./img/slide3.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file)

        btn = types.InlineKeyboardButton('Выбрать',callback_data='CardReveal')
        markup = types.InlineKeyboardMarkup()
        markup.add(btn)

        bot.send_message(callback.message.chat.id, text, reply_markup=markup)
    elif callback.data == 'CardReveal':
        f = open('./db_back.json',encoding="utf8")
        data = json.load(f)
        random_card = random.randrange(1, len(data["cards"]), 1)

        file = open('./img/' + data['cards'][random_card]['name'] + '.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file)
        file.close()

        bot.send_message(callback.message.chat.id, data['cards'][random_card]['description'])
        f.close()
    elif callback.data == 'Zodiac':
        text = 'Выбор сделан... Звезды готовы рассказать вам о том, что они приготовили для вас. Прогноз по гороскопу откроет вам небесные секреты и поможет лучше понять, как использовать их в свою пользу.'
        print("Horoscope")
        bot.send_message(callback.message.chat.id,text)
    elif callback.data == 'Affirmation':
        text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии.'
        print("Affirmation")
        bot.send_message(callback.message.chat.id,text)






bot.polling(none_stop=True)

