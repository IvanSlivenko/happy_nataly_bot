

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, callback_query, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
import json

#------------------------------------------------------- initial bot
from config import TOKEN, PAYMENT_TOKEN
from config import url_Bild_Expr, url_Bild_Expr_doors, url_custome_1, url_Bild_Expr_heating
#---------------------------------------- TOKEN
bot = Bot(TOKEN)
dp = Dispatcher()
#-------------------------------------------------------

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_invoice(
        chat_id= message.chat.id,
        title="Велосипед",
        description="Спортивний Велосипед",
        payload=f'invoice',
        provider_token=str(PAYMENT_TOKEN),
        currency='UAH',
        prices=[
            types.LabeledPrice(
                label='Вартість',
                amount=5000*100
            )
        ],
        # max_tip_amount=100*100,
        # suggested_tip_amounts=[10000,30000],
        # start_parameter=f'testpaymentbot',
        # provider_data=None,
        # need_email=True,
        # need_phone_number=True,
        # need_name=True,
        # need_shipping_address=False,
        # send_phone_number_to_provider=False,
        # send_email_to_provider=False,
        # is_flexible=False,
        # disable_notification=False,
        # protect_content=True,
        # reply_to_message_id=None,
        # allow_sending_without_reply=True,
        # reply_markup=None,
        # request_timeout=30
    )

@dp.message(F.types.ContentType.SUCCESSFUL_PAYMENT)
async def succes(message: types.Message):
    await message.answer(f'Succes {message.successful_payment.order_info}')




#----------------------------------------- run
async def main():
    
    
    await dp.start_polling(bot)

if __name__  == '__main__':
    print('Бот розпочав роботу')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот вимкнуто')    
