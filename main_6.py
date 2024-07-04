import telebot
import webbrowser
import sqlite3
import pygame
import requests
import json

from currency_converter import CurrencyConverter
from pyrrencies import CurrencyRates

from telebot import types



from config import TOKEN




bot = telebot.TeleBot(TOKEN)
currency=CurrencyConverter()
currency_2=CurrencyRates

amountn = 0 #-----------------------------------оголошуємо глобальну змінну

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,f'{message.from_user.first_name}\nВітаємо\nВкажіть сумму конвертації')#--------------- пишемо повідомлення користувачц
    bot.register_next_step_handler(message, summa)#------------------одноразово запускаємо функцію summ

def summa(message):
    global amount #----------------------------------------------------------- викликаємо глобальну змінну

    try:
        amount = int(message.text.strip())#------------------stpip() видаляє пробіли
    except ValueError:
        bot.send_message(message.chat.id,'Не вірний формат, вкажіть суму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)#------------------------------ створюємо клавіатуру
        
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')#------------------------- створюємо кнопки
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/UAH', callback_data='usd/uah')
        btn4 = types.InlineKeyboardButton('UAH/USD', callback_data='uah/usd')
        btn5 = types.InlineKeyboardButton('Інше значення',callback_data='else')

        markup.add(btn1, btn2, btn3, btn4, btn5)#---------------------------------додаємо кнопки вклавіатуру

        bot.send_message(message.chat.id,'Оберіть потрібну пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,'Число має бути більше 0,  вкажіть вірну суму')
        bot.register_next_step_handler(message, summa)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_metod(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        bot.send_message(call.message.chat.id, 'Проводимо розрахунок')
        res_currency = round(currency_2.get_rate(values[0], values[1]),2)
        res_summ = round(amount * res_currency,2)
        

        bot.send_message(call.message.chat.id, f'Під час конвертації {amount} {values[0]} в {values[1]} по курсу {res_currency}  ви отримаєте {res_summ}  {values[1]}.\n можете знову вказати сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
         bot.send_message(call.message.chat.id, 'Вкажіть пару значень через /')
         bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res_currency = round(currency_2.get_rate(values[0], values[1]),2)
        res_summ = round(amount * res_currency,2)
        

        bot.send_message(message.chat.id, 'Уважно Вкажіть пару значень через /')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Під час конвертації {amount} {values[0]} в {values[1]} по курсу {res_currency}  ви отримаєте {res_summ}  {values[1]}.\n можете знову вказати сумму')
        bot.register_next_step_handler(message, my_currency)


    

    


    






#----------------------------------------- run
def main():
    print('Почався запуск бота')
    bot.polling(non_stop=True)

main()
