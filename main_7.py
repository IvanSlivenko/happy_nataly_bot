

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, callback_query, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

#------------------------------------------------------- initial bot
from config import TOKEN
#---------------------------------------- TOKEN
bot = Bot(TOKEN)
dp = Dispatcher()
#-------------------------------------------------------









@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Hello')

#-----------------------------------------------------------------------Відправляємо фото та текст у відповідь
@dp.message(F.text == 'test')
async def test(message: types.Message):
    await message.reply('the test is started')
    file = FSInputFile('./images/Screenshot_1.jpg', 'rb')
    await message.answer_photo(photo=file)   

#------------------------------------------------------------------------ Створюємо Replay button 
@dp.message(F.text == 'rbt')
async def replay_button(message: types.Message):
    # await message.answer('rbt')
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text='Site'))
    markup.add(KeyboardButton(text='Contacts'))  
    await message.answer('Оберіть', reply_markup=markup.adjust(2,).as_markup(resize_keyboard=True))

#---------------------------------------------------------------------------Створюємо Inline button
@dp.message(F.text == 'ibt')
async def inline_button(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Google", callback_data='Google')
    builder.button(text="Set", callback_data="set")
    builder.adjust(2, )
    await message.answer("Some text here", reply_markup=builder.as_markup())

#--------------------------------------------------------------------------------------- Ловимо Callback.data
@dp.callback_query(F.data.startswith('Google'))
# @dp.callback_query()#------------------------------------------------------ Ловимо всі Callback 
async def callback_query_handler(callback: types.CallbackQuery):
    
    await callback.message.answer(f'Буде здійснено перехід на {callback.data}')
#--------------------------------------------------------------------------------------- Ловимо Callback.data
@dp.callback_query(F.data.startswith('set'))
# @dp.callback_query()
async def callback_query_handler_2(callback: types.CallbackQuery):
    await callback.message.answer(f'Ви натиснули кнопку {callback.data}')    
    



    
   




   


#----------------------------------------- run
async def main():
    
    
    await dp.start_polling(bot)

if __name__  == '__main__':
    print('Бот розпочав роботу')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот вимкнуто')    
