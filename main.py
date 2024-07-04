import telebot
import webbrowser
import sqlite3
import pygame
import requests
import json


from telebot import types

from config import TOKEN
from config import WEATHER_KEY

url_judo='https://www.google.com/search?client=opera&q=lp.lj+evfym&sourceid=opera&ie=UTF-8&oe=UTF-8#lpg=cid:CgIgAQ%3D%3D,ik:CAoSLEFGMVFpcFBEZklZWmFHQTJUQk5rRmNRRWdvSlBiRGxrT2ZWM1hyWC15SFpa'
url_Google='https://www.google.com/?hl=ru'

url_Bild_Expr='https://bud-express.in.ua'
url_Bild_Expr_doors='https://bud-express.in.ua/categories/d38241db-946c-4fbc-8338-eba2e95ade7e'
url_Bild_Expr_heating='https://bud-express.in.ua/categories/43dbb77f-d0a2-46f2-bd47-fb5786073407'


bot = telebot.TeleBot(TOKEN)

#----------------------------------------------------------------- weather button beginning
@bot.message_handler(commands=['wt'])
def use_wt_button(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Погода', callback_data='weather'))

    file = open('./images/3.png', 'rb')
    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}. Вітаємо. Натисніть кнопку для перегляду погоди', reply_markup=markup)

@bot.callback_query_handler(func= lambda callback: True)
def callback_weather(callback):

    if callback.data == 'weather':
        bot.send_message(callback.message.chat.id, 'Вітаємо. Вкажіть місце подорожі')
        bot.register_next_step_handler(callback.message, get_weather) #----------- реєструємо одноразове використання функції
        

#---------------------------------------------------------------------------------------------------------------------- weather button end

#----------------------------------------------------------------------------------------------------------- weather beginning
# @bot.message_handler(commands=['weat'])
# def weat(message):
#     bot.send_message(message.chat.id, f'{message.from_user.first_name}. Вітаємо. Вкажіть місце подорожі')

# @bot.message_handler(content_types='text')
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

#-------------------------------------------------------------------------------- site
current_name=None #------------------ об'являємо глобальну змінну
#-------------------

@bot.message_handler(commands=['start'])
def go_to_site(message):
   
    file = open('./images/logo.webp','rb')
    # file = open('./images/TAA.png','rb')    
    bot.send_photo(message.chat.id, file, caption=f'{message.from_user.first_name} - вітаємо в Буд експрес Умань')
    # bot.send_photo(message.chat.id, file, caption=f'{message.from_user.first_name} - вітаємо з Днем народження')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('На сайт 👉', url=url_Bild_Expr))

    btn_2=types.InlineKeyboardButton('Двері 🚪', url=url_Bild_Expr_doors)
    btn_3=types.InlineKeyboardButton('Опалення 🏭', url=url_Bild_Expr_heating)
    
    markup.row(btn_2, btn_3)

    bot.send_message(message.chat.id, 'Асортимент товарів ви можете переглянути на сайті', reply_markup=markup)
    # bot.send_message(message.chat.id, 'Тут ви можете переглянути ваші сайти', reply_markup=markup)  


#---------------------------------------------------------------- use db

@bot.message_handler(commands=['db'])
def use_db(message):

    conn = sqlite3.connect('db.sqlite3')#----------- coonct to db
    cur = conn.cursor()#----------------------- create cursor

    # commands
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER primary key, name varchar(50), password varchar(50))')
    
    conn.commit()#-----------------self

    cur.close()# exit cursor
    conn.close()# exit connect

    bot.send_message(message.chat.id, f"{message.from_user.first_name}\n Ми починаємо вашу реєстрацію.\n\
                  Вкажіть ваше ім'я")
    bot.register_next_step_handler(message, user_name) #----------- реєструємо одноразове використання функції

def user_name(message):
    global current_name #--------- викликаємо глобальну змінну
    current_name = message.text.strip()
    bot.send_message(message.chat.id, "Вкажіть пароль")
    bot.register_next_step_handler(message, user_pass) #----------- реєструємо одноразове використання функції

def user_pass(message):
    current_password = message.text.strip()

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, password) VALUES ('%s', '%s')" % (current_name, current_password))
    conn.commit()

    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список користувачів', callback_data='users'))
    bot.send_message(message.chat.id, f"{message.from_user.first_name}\n Ви зареєстровані" , reply_markup=markup)
   
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f"id: {el[0]}   Ім'я: {el[1]}   пароль : {el[2]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


#--------------------------------------------------------------------------------------------- start on_click
@bot.message_handler(commands=['start1'])
def cmd_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton('Сайт Буд Експрес'))

    btn_2=types.KeyboardButton('Видалити фото')
    btn_3=types.KeyboardButton('Редагувати текст')
    
    markup.row(btn_2, btn_3)

#--------------------------------------------------------------------------------------------- audio file
    # file_audio = open('./images/vinny.mp3','rb')
    # pygame.mixer.init()
    # pygame.mixer.music.load(file_audio)
    # pygame.mixer.music.play()
    # bot.send_audio(message.chat.id, file_audio , reply_markup=markup)
#-----------------------------------------------------------------------------

    file = open('./images/logo.webp','rb')  
    bot.send_photo(message.chat.id, file, caption=f'Вітаємо {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    # if message.text == 'Сайт Буд Експрес':
    if message.text == 'test':
        webbrowser.open(url_Bild_Expr)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}\n Можете переглянути потрібну сторінку в браузері')
        # bot.send_message(message.chat.id, 'Website is open')   
    elif message.text == 'Видалити фото':
        bot.send_message(message.chat.id, 'delete')
    elif message.text == 'Редагувати текст':
        bot.send_message(message.chat.id, 'edit')    
#----------------------------------------------------------------------- end on_click

#---------------------------------------------------------------------------------------------------- photo
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Google', url=url_Google))

    btn_1=types.InlineKeyboardButton('Перейти на сайт', url=url_Bild_Expr)

    markup.row(btn_1)

    btn_2=types.InlineKeyboardButton('Видалити фото', callback_data='delete')
    btn_3=types.InlineKeyboardButton('Редагувати текст', callback_data='edit')
    
    markup.row(btn_2, btn_3)
    
    # bot.reply_to(message, 'Контент для вашого перегляду', reply_markup=markup)
    bot.send_message(message.chat.id, 'Контент для вашого перегляду', reply_markup=markup)     
    

@bot.callback_query_handler(func= lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)    



@bot.message_handler(commands=['site', 'website'])
def site(message):
    
    webbrowser.open(url_Bild_Expr)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}\n Можете переглянути потрібну сторінку в браузері')
    

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')

@bot.message_handler(commands=['info'])
def cmd_info(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}\n Вітаємо у нас на платформі' )

         

#----------------------------------------- total text    
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привіт':
        bot.send_message(message.chat.id, f'{message.from_user.first_name}\n Вітаємо у нас на платформі')

    elif message.text.lower() == 'p24':
        bot.send_message(message.chat.id, f'{message.from_user.first_name}\n Можете переглянути потрібну сторінку в браузері')
        webbrowser.open('https://next.privat24.ua')

    elif message.text.lower() == 'id':
        bot.reply_to(message, f' id :{message.from_user.id}')


#----------------------------------------- run
def main():
    print('Почався запуск бота')
    bot.polling(non_stop=True)

main()
