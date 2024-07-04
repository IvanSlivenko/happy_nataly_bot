import telebot
import webbrowser
import sqlite3
import pygame
import requests
import json


from telebot import types

from config import TOKEN
from config import WEATHER_KEY



bot = telebot.TeleBot(TOKEN)



#----------------------------------------------------------------------------------------------------------- weather beginning
@bot.message_handler(commands=['weat'])
def weat(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}. Вітаємо. Вкажіть місце подорожі')

@bot.message_handler(content_types='text')
def get_weather(message):
    city = message.text.strip().lower()
   
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric')
    data = json.loads(res.text)
    
    if res.status_code == 200:
    
        # bot.send_message(message.chat.id, f' Параметри погоди : {res.json()}')#----------------------------------------- all parametrs
        
        #--------------------------------------------------------------------- Банер погоди
        clouds = data['clouds']['all']
        image_1 = '1.jpg'
        image_2 = '2.webp'

        image = '1.jpg' if clouds <= 80 else '2.webp'
        file= open('./images/'+ image, 'rb')
        bot.send_photo(message.chat.id, file)
        #--------------------------------------------------------------------- Параметри погоди
        bot.send_message(message.chat.id, f"Погода {city}:\n\
                                Мінімальна температура :  {data['main']['temp_min']} град.С \n\
                                Максимальна тепмература :  {data['main']['temp_max']} град.C \n\
                                Атмосферний тиск :  {data['main']['pressure']} мм. \n\
                                Вологістть :  {data['main']['humidity']} % \n\
                                Хмарність :  {data['clouds']['all']} % \n\
                                Швидкість вітру: {data['wind']['speed']} м.с. \n\
                                ")
    else:
        bot.send_message(message.chat.id, f'Місто з пошуковим запитом : {city} не знайдено')
#-------------------------------------------------------------------------------------------------------- weather end

#----------------------------------------- run
def main():
    print('Почався запуск бота')
    bot.polling(non_stop=True)

main()
