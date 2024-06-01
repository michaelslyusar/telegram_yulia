import types

import telebot
from dotenv import load_dotenv
import os
import sqlite3
from telebot import types

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
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('Продолжать'))
    
    bot.send_message(message.chat.id,text,reply_markup=markup)
    bot.register_next_step_handler(message, main_menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'tarot':
        bot.send_message(callback.message.chat.id,'Tarot')



def main_menu(message):
    file=open('./img/slide2.jpg','rb')
    bot.send_photo(message.chat.id,file)

    markup = types.InlineKeyboardMarkup()
    btn_tarot = types.InlineKeyboardButton('Карта дня', callback_data='Tarot')

    markup.add(btn_tarot)

    bot.send_message(message.chat.id, '', reply_markup=markup)


bot.polling(none_stop=True)

#