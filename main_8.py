

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, callback_query, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
import json

#------------------------------------------------------- initial bot
from config import TOKEN
from config import url_Bild_Expr, url_Bild_Expr_doors, url_custome_1, url_Bild_Expr_heating
#---------------------------------------- TOKEN
bot = Bot(TOKEN)
dp = Dispatcher()
#-------------------------------------------------------



@dp.message(CommandStart())
#-------------------------------------------------------------------------------------   inlain keyboard
# async def cmd_start(message: types.Message):
#     markup = InlineKeyboardBuilder()
#     markup.add(InlineKeyboardButton(text='BudExpress', web_app=WebAppInfo(url=str(url_Bild_Expr))))
#     markup.add(InlineKeyboardButton(text='BudExpress Двері', web_app=WebAppInfo(url=str(url_Bild_Expr_doors))))
#     markup.add(InlineKeyboardButton(text='BudExpress Опалення', web_app=WebAppInfo(url=str(url_Bild_Expr_heating))))
#     markup.add(InlineKeyboardButton(text='Home page', web_app=WebAppInfo(url=str(url_custome_1))))
#     markup.add(InlineKeyboardButton(text='Google', web_app=WebAppInfo(url='https://www.google.com.ua/?hl=uk')))
    
#     await message.answer(f'{message.from_user.first_name}. Вітаємо !', reply_markup=markup.adjust(1,2,1,1).as_markup(resize_keyboard=True))
    
#-------------------------------------------------------------------------------------   replay keyboard
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text='BudExpress', web_app=WebAppInfo(url=str(url_Bild_Expr))))
    markup.add(KeyboardButton(text='BudExpress Двері', web_app=WebAppInfo(url=str(url_Bild_Expr_doors))))
    markup.add(KeyboardButton(text='BudExpress Опалення', web_app=WebAppInfo(url=str(url_Bild_Expr_heating))))
    markup.add(KeyboardButton(text='Home page', web_app=WebAppInfo(url=str(url_custome_1))))
    markup.add(KeyboardButton(text='Google', web_app=WebAppInfo(url='https://www.google.com.ua/?hl=uk')))
    
    await message.answer(f'{message.from_user.first_name}. Вітаємо !', reply_markup=markup.adjust(1,2,1,1).as_markup(resize_keyboard=True))    




#-----------------------------------------------------------------------Відправляємо фото та текст у відповідь
@dp.message(F.text == 'test')
async def test(message: types.Message):
    await message.reply('the test is started')
    file = FSInputFile('./images/Screenshot_1.jpg', 'rb')
    await message.answer_photo(photo=file)   

@dp.message(F.web_app_data)
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'name: {res["name"]}. email: {res["email"]}. phpne: {res["phone"]}')


    



    
   




   


#----------------------------------------- run
async def main():
    
    
    await dp.start_polling(bot)

if __name__  == '__main__':
    print('Бот розпочав роботу')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот вимкнуто')    
