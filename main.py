# -*- coding: utf-8 -*-
import types
import json
import time
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
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment PRIMARY KEY, user_id varchar(50),last_affirmation date,last_zodiac date, last_tarot_read date)')
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
    file = open('./img/affirmation.jpg', 'rb')
    bot.send_photo(message.chat.id, file)
    file.close()

    text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии.'
    bot.send_message(message.chat.id, text)

    f = open('db.json', encoding="utf8")
    data = json.load(f)
    random_affirmation = random.randrange(1, len(data["Affirmations"]), 1)
    print(len(data["Affirmations"]))
    bot.send_message(message.chat.id, data["Affirmations"][random_affirmation]["text"])
    f.close()

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
        f = open('db.json', encoding="utf8")
        data = json.load(f)
        random_card = random.randrange(1, len(data["cards"]), 1)
        print(len(data["cards"]))
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
        file = open('./img/affirmation.jpg','rb')
        bot.send_photo(callback.message.chat.id, file)
        file.close()

        text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии.'
        bot.send_message(callback.message.chat.id, text)

        f = open('db.json', encoding="utf8")
        data = json.load(f)
        random_affirmation = random.randrange(1, len(data["Affirmations"]), 1)
        print(callback.message)
        bot.send_message(callback.message.chat.id, data["Affirmations"][random_affirmation]["text"])
        f.close()

        user_id = callback.message.chat.id
        date = callback.message.date
        set_affirmation_date(user_id)

def set_affirmation_date(user_id):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO users(user_id,last_affirmation) VALUES("%s","%s")' % (user_id,time.time()))
    conn.commit()
    cur.close()
    conn.close()




bot.polling(none_stop=True)

