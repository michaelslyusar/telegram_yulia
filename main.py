import types

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

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment PRIMARY KEY, user_id varchar(50), last_tarot_read date)')
    conn.commit()
    cur.close()
    conn.close()

    file = open('./img/slide1.jpg','rb')
    bot.send_photo(message.chat.id,file)

    text = 'Добро пожаловать, странник!✨ На пороге волшебного мира вас встречает мудрый маг. Под светом луны и сиянием звезд он проведет вас через тайны и откровения.🌙Приготовьтесь к удивительному путешествию, где каждое предсказание откроет новые грани вашей души и сердца. Позвольте магу стать вашим проводником в мир предсказаний и мудрости'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(types.KeyboardButton('Продолжать'))
    
    bot.send_message(message.chat.id,text,reply_markup=markup)
    bot.register_next_step_handler(message, main_menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'Tarot':
        text = '"Выбор сделан... Карта дня откроет вам завесу будущего и покажет, какие энергии и события ждут вас сегодня. Позвольте магу раскрыть перед вами тайны этого дня и получить важное предсказание."'
        print("tarot")
        random_card = random.randrange(1, 13, 1)

        bot.send_message(callback.message.chat.id, text)

        file = open('./img/'+str(random_card)+'.jpg','rb')
        bot.send_photo(callback.message.chat.id,file)

        bot.send_message(callback.message.chat.id, 'Tarot prediction')

    elif callback.data == 'Horoscope':
        text = '"Выбор сделан... Звезды готовы рассказать вам о том, что они приготовили для вас. Прогноз по гороскопу откроет вам небесные секреты и поможет лучше понять, как использовать их в свою пользу."'
        print("Horoscope")
        bot.send_message(callback.message.chat.id,text)
    elif callback.data == 'Affirmation':
        text = '"Выбор сделан... Мудрый маг приготовил для вас аффирмацию, которая наполнит ваш день позитивной энергией и вдохновением. Повторяйте её, чтобы укрепить свой дух и достичь гармонии."'
        print("Affirmation")
        bot.send_message(callback.message.chat.id,text)



def main_menu(message):
    file=open('./img/slide2.jpg','rb')
    bot.send_photo(message.chat.id,file)

    markup = types.InlineKeyboardMarkup()
    btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Tarot')
    btn_horoscope= types.InlineKeyboardButton('Прогноз по гороскопу',callback_data='Horoscope')
    btn_affirmation= types.InlineKeyboardButton('Аффирмация дня',callback_data='Affirmation')

    markup.row(btn_tarot)
    markup.row(btn_horoscope,btn_affirmation)

    text = 'Text for main menu'
    bot.send_message(message.chat.id, text, reply_markup=markup)


bot.polling(none_stop=True)

#