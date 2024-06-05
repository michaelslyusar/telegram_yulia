# -*- coding: utf-8 -*-
import types
import math
import json
import datetime
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
    try:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS users(user_id varchar(50) PRIMARY KEY,last_affirmation date,last_zodiac date, last_tarot_read date)')
        cur.execute('INSERT INTO users(user_id) VALUES(:user_id)', {'user_id': message.chat.id})
    except Exception as e:
        print('Something went wrong when initializing DB or user')
        print(e)
    conn.commit()
    cur.close()
    conn.close()

    file = open('img/slide2.jpg', 'rb')
    bot.send_photo(message.chat.id, file)

    markup = types.InlineKeyboardMarkup()
    btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
    btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
    btn_affirmation = types.InlineKeyboardButton('Аффирмация дня', callback_data='Affirmation')

    markup.row(btn_tarot)
    markup.row(btn_horoscope, btn_affirmation)

    text = """Мудрый маг предлагает вам выбрать путь:

Откройте карту дня и узнайте, что ждёт вас впереди
🔮 /card

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
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['zodiac'])
def zodiac(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('\u2651Козерог', callback_data='Zodiac')
    btn2 = types.InlineKeyboardButton('\u2652Водолей', callback_data='Zodiac')
    btn3 = types.InlineKeyboardButton('\u2653Рыбы', callback_data='Zodiac')
    btn4 = types.InlineKeyboardButton('\u2648Овен', callback_data='Zodiac')
    btn5 = types.InlineKeyboardButton('\u2649Телец', callback_data='Zodiac')
    btn6 = types.InlineKeyboardButton('\u264AБлизнецы', callback_data='Zodiac')
    btn7 = types.InlineKeyboardButton('\u264BРак', callback_data='Zodiac')
    btn8 = types.InlineKeyboardButton('\u264CЛев', callback_data='Zodiac')
    btn9 = types.InlineKeyboardButton('\u264DДева', callback_data='Zodiac')
    btn10 = types.InlineKeyboardButton('\u264EВесы', callback_data='Zodiac')
    btn11 = types.InlineKeyboardButton('\u264FСкорпион', callback_data='Zodiac')
    btn12 = types.InlineKeyboardButton('\u2650Стрелец', callback_data='Zodiac')

    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    markup.row(btn7, btn8, btn9)
    markup.row(btn10, btn11, btn12)

    text = 'Выбор сделан... Звезды готовы рассказать вам о том, что они приготовили для Вас в этом году.'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['affirmation'])
def affirmation(message):
    try:
        daily_access = check_last_affirmation(message.chat.id)
        if daily_access:
            markup = types.InlineKeyboardMarkup()
            btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
            btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
            markup.row(btn_tarot, btn_horoscope)

            file = open('./img/affirmation.jpg', 'rb')
            bot.send_photo(message.chat.id, file)
            file.close()

            text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии:'

            f = open('db.json', encoding="utf8")
            data = json.load(f)
            random_affirmation = random.randrange(1, len(data["Affirmations"]), 1)
            bot.send_message(message.chat.id,
                             text + "\n\n" + data["Affirmations"][random_affirmation]["text"],
                             parse_mode='HTML', reply_markup=markup)
            f.close()

            user_id = message.chat.id
            try:
                set_affirmation_date(user_id)
            except:
                print('something went wrong when updating affirmations in db')

            markup = types.ReplyKeyboardMarkup()
            btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
            btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
            markup.row(btn_tarot, btn_horoscope)
        else:
            # Affirmation access denied
            # Image
            file = open('./img/affirmation_denied.jpg', 'rb')
            bot.send_photo(message.chat.id, file)
            file.close()
            # Buttons
            markup = types.InlineKeyboardMarkup()
            btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
            btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
            markup.row(btn_horoscope, btn_tarot)
            # Text
            text = '<b>Мудрый маг глядит на вас с понимающей улыбкой и произносит:</b>\n«Сегодня ваша аффирмация уже выбрана. Слова мудрости и силы, которые вы получили, предназначены именно для вас в этот день. Повторить выбор нельзя, ведь каждая аффирмация несет свою уникальную энергию и значение. Возвращайтесь завтра, и судьба откроет перед вами новые слова вдохновения.»'
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
    except:
        print('something went wrong when checking last affirmation')


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'Card':
        text = 'Выбор сделан... Карта дня откроет вам завесу будущего и покажет, какие энергии и события ждут вас сегодня. Позвольте магу раскрыть перед вами тайны этого дня и получить важное предсказание.'

        file = open('./img/slide3.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file)

        btn = types.InlineKeyboardButton('Выбрать', callback_data='CardReveal')
        markup = types.InlineKeyboardMarkup()
        markup.add(btn)

        bot.send_message(callback.message.chat.id, text, reply_markup=markup)

    elif callback.data == 'CardReveal':
        try:
            daily_access = check_last_tarot_read(callback.message.chat.id)
            if daily_access:
                # Picking random card from card list
                f = open('db.json', encoding="utf8")
                data = json.load(f)
                random_card = random.randrange(1, len(data["cards"]), 1)
                f.close()

                # Gui
                # Image
                file = open('./img/' + data['cards'][random_card]['name'] + '.jpg', 'rb')
                bot.send_photo(callback.message.chat.id, file)
                file.close()
                # Buttons
                markup = types.InlineKeyboardMarkup()
                btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
                btn_affirmation = types.InlineKeyboardButton('Аффирмация дня', callback_data='Affirmation')
                markup.row(btn_affirmation, btn_horoscope)
                bot.send_message(callback.message.chat.id, data['cards'][random_card]['description'],
                                 reply_markup=markup)

                # Updating date of last tarot
                user_id = callback.message.chat.id
                try:
                    set_tarot_read_date(user_id)
                except:
                    print('something went wrong when updating last tarot read in db')
            else:
                # Card Access Denies
                # Image
                file = open('./img/card_denied.jpg', 'rb')
                bot.send_photo(callback.message.chat.id, file)
                file.close()
                # Buttons
                markup = types.InlineKeyboardMarkup()
                btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
                btn_affirmation = types.InlineKeyboardButton('Аффирмация дня', callback_data='Affirmation')
                markup.row(btn_horoscope,btn_affirmation)
                # Text
                text ='<b>Мудрый маг глядит на вас с глубоким пониманием и говорит:</b>\n«Сегодня ваш выбор уже сделан. Судьба развернулась перед вами, и её тайны раскрылись. Повторить выбор нельзя, ведь мудрость приходит лишь тем, кто умеет ждать. Возвращайтесь завтра, когда звезды вновь будут благосклонны к вам.»'
                bot.send_message(callback.message.chat.id, text, reply_markup=markup,parse_mode='HTML')
                print('tarot access denied')
        except:
            print('Something went wrong while checking for last tarot read')

    elif callback.data == 'ZodiacSelection':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('\u2651Козерог', callback_data='Гороскоп_Козерог')
        btn2 = types.InlineKeyboardButton('\u2652Водолей', callback_data='Гороскоп_Водолей')
        btn3 = types.InlineKeyboardButton('\u2653Рыбы', callback_data='Гороскоп_Рыбы')
        btn4 = types.InlineKeyboardButton('\u2648Овен', callback_data='Гороскоп_Овен')
        btn5 = types.InlineKeyboardButton('\u2649Телец', callback_data='Гороскоп_Телец')
        btn6 = types.InlineKeyboardButton('\u264AБлизнецы', callback_data='Гороскоп_Близнецы')
        btn7 = types.InlineKeyboardButton('\u264BРак', callback_data='Гороскоп_Рак')
        btn8 = types.InlineKeyboardButton('\u264CЛев', callback_data='Гороскоп_Лев')
        btn9 = types.InlineKeyboardButton('\u264DДева', callback_data='Гороскоп_Дева')
        btn10 = types.InlineKeyboardButton('\u264EВесы', callback_data='Гороскоп_Весы')
        btn11 = types.InlineKeyboardButton('\u264FСкорпион', callback_data='Гороскоп_Скорпион')
        btn12 = types.InlineKeyboardButton('\u2650Стрелец', callback_data='Гороскоп_Стрелец')

        markup.row(btn1, btn2, btn3)
        markup.row(btn4, btn5, btn6)
        markup.row(btn7, btn8, btn9)
        markup.row(btn10, btn11, btn12)

        text = 'Выбор сделан... Звезды готовы рассказать вам о том, что они приготовили для Вас в этом году.'
        bot.send_message(callback.message.chat.id, text, reply_markup=markup)

    elif callback.data == 'Affirmation':
        try:
            daily_access = check_last_affirmation(callback.message.chat.id)
            print(daily_access)
            if daily_access:
                print('if')
                markup = types.InlineKeyboardMarkup()
                btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
                btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
                markup.row(btn_tarot, btn_horoscope)

                file = open('./img/affirmation.jpg', 'rb')
                bot.send_photo(callback.message.chat.id, file)
                file.close()

                text = 'Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии:'

                f = open('db.json', encoding="utf8")
                data = json.load(f)
                random_affirmation = random.randrange(1, len(data["Affirmations"]), 1)
                print(callback.message)
                bot.send_message(callback.message.chat.id,
                                 text + "\n\n" + data["Affirmations"][random_affirmation]["text"],
                                 parse_mode='HTML', reply_markup=markup)
                f.close()

                user_id = callback.message.chat.id
                try:
                    set_affirmation_date(user_id)
                except:
                    print('something went wrong when updating affirmations in db')

                markup = types.ReplyKeyboardMarkup()
                btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
                btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
                markup.row(btn_tarot, btn_horoscope)
            else:
                # Affirmation access denied
                # Image
                file = open('./img/affirmation_denied.jpg', 'rb')
                bot.send_photo(callback.message.chat.id, file)
                file.close()
                # Buttons
                markup = types.InlineKeyboardMarkup()
                btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
                btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
                markup.row(btn_horoscope, btn_tarot)
                # Text
                text = '<b>Мудрый маг глядит на вас с понимающей улыбкой и произносит:</b>\n«Сегодня ваша аффирмация уже выбрана. Слова мудрости и силы, которые вы получили, предназначены именно для вас в этот день. Повторить выбор нельзя, ведь каждая аффирмация несет свою уникальную энергию и значение. Возвращайтесь завтра, и судьба откроет перед вами новые слова вдохновения.»'
                bot.send_message(callback.message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        except:
            print('something went wrong when checking last affirmation')

    elif callback.data == 'Гороскоп_Козерог':
        horoscope('Козерог', callback.message)

    elif callback.data == 'Гороскоп_Водолей':
        horoscope('Водолей', callback.message)

    elif callback.data == 'Гороскоп_Рыбы':
        horoscope('Рыбы', callback.message)

    elif callback.data == 'Гороскоп_Овен':
        horoscope('Овен', callback.message)

    elif callback.data == 'Гороскоп_Телец':
        horoscope('Телец', callback.message)

    elif callback.data == 'Гороскоп_Близнецы':
        horoscope('Близнецы', callback.message)

    elif callback.data == 'Гороскоп_Рак':
        horoscope('Рак', callback.message)

    elif callback.data == 'Гороскоп_Лев':
        horoscope('Лев', callback.message)

    elif callback.data == 'Гороскоп_Дева':
        horoscope('Дева', callback.message)

    elif callback.data == 'Гороскоп_Весы':
        horoscope('Весы', callback.message)

    elif callback.data == 'Гороскоп_Скорпион':
        horoscope('Скорпион', callback.message)

    elif callback.data == 'Гороскоп_Стрелец':
        horoscope('Стрелец', callback.message)


def set_affirmation_date(user_id):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()
    try:
        cur.execute('UPDATE users SET last_affirmation = :time WHERE user_id = :user_id',
                    {'user_id': user_id, 'time': time.time()})
    except Exception as e:
        print(e)
    conn.commit()
    cur.close()
    conn.close()


def set_tarot_read_date(user_id):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()
    try:
        cur.execute('UPDATE users SET last_tarot_read = :time WHERE user_id = :user_id',
                    {'user_id': user_id, 'time': time.time()})
    except Exception as e:
        print(e)
    conn.commit()
    cur.close()
    conn.close()


def check_last_affirmation(user_id):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE user_id=:user_id', {'user_id': user_id})
        user = cur.fetchone()
        if (user[1] is None):
            return True
    except Exception as e:
        print(e)
    conn.commit()
    cur.close()
    conn.close()

    # Adding restriction for daily affirmation at 6AM
    # Checking whether current date and last affirmation dates are the same
    if (datetime.datetime.fromtimestamp(user[1]).date() == datetime.date.today()):
        if (datetime.datetime.now().hour >= 6):
            if (datetime.datetime.fromtimestamp(user[1]).time().hour < 6):
                return True
            else:
                return False
        else:
            return False
    # Checking whether last affirmation was done the day before
    elif (datetime.datetime.fromtimestamp(user[1]).date() == datetime.date.today() - datetime.timedelta(days=1)):
        if (datetime.datetime.now().hour < 6):
            if (datetime.datetime.fromtimestamp(user[1]).time().hour < 6):
                return True
            else:
                return False
        else:
            return True
    else:
        return True


def check_last_tarot_read(user_id):
    conn = sqlite3.connect('mysticism.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM users WHERE user_id=:user_id', {'user_id': user_id})
        user = cur.fetchone()
        if(user[3] is None):
            return True
    except Exception as e:
        print(e)
    conn.commit()
    cur.close()
    conn.close()

    # Adding restriction for daily affirmation at 6AM
    # Checking whether current date and last affirmation dates are the same
    if (datetime.datetime.fromtimestamp(user[3]).date() == datetime.date.today()):
        if (datetime.datetime.now().hour >= 6):
            if (datetime.datetime.fromtimestamp(user[3]).time().hour < 6):
                return True
            else:
                return False
        else:
            return False
    # Checking whether last affirmation was done the day before
    elif (datetime.datetime.fromtimestamp(user[3]).date() == datetime.date.today() - datetime.timedelta(days=1)):
        if (datetime.datetime.now().hour < 6):
            if (datetime.datetime.fromtimestamp(user[3]).time().hour < 6):
                return True
            else:
                return False
        else:
            return True
    else:
        return True


def horoscope(sign, message):
    f = open('db.json', encoding="utf8")
    file = open('./img/zodiac.jpg', 'rb')
    data = json.load(f)

    markup = types.InlineKeyboardMarkup()
    btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Card')
    btn_horoscope = types.InlineKeyboardButton('Гороскоп на 2024', callback_data='ZodiacSelection')
    btn_affirmation = types.InlineKeyboardButton('Аффирмация дня', callback_data='Affirmation')
    markup.row(btn_affirmation, btn_tarot)
    markup.row(btn_horoscope)

    text = data['Zodiac'][sign]

    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
    f.close()
    file.close()


bot.polling(none_stop=True)
