import asyncio
import os

from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.default.adminKey import adminusers,admincommands
from keyboards.inline.inlinekey import rek


@dp.message_handler(text="/start", user_id=ADMINS)
async def get_all_users(message: types.Message):

    #await message.answer('admin panel',reply_markup=admincommands)
    await bot.send_message(chat_id=ADMINS[0],text='Siz adminsiz',reply_markup=admincommands)




@dp.message_handler(text="admin panel", user_id=ADMINS)
async def get_all_users(message: types.Message):

    await message.answer('admin panel',reply_markup=adminusers)




@dp.message_handler(text="users", user_id=ADMINS)
async def get_all_users(message: types.Message):
    count = db.count_users()
    users = db.select_all_users()
    text = f"instabot || Foydalanuvchilar soni: {count[0]}\n\n"
    for user in users:
        text+= f"{user[0]}). || {user[2]} || @{user[3]} || {user[4]}\n"
    await message.answer(text)


@dp.message_handler(text="back", user_id=ADMINS)
async def back_button(message: types.Message):

    await message.answer('Bosh menyu',reply_markup=admincommands)



@dp.message_handler(text="reklama",user_id=ADMINS)
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("reklama yuboring")
    await state.set_state("reklama")



@dp.message_handler(state='reklama')
async def send_ad_to_all(message: types.Message,state: FSMContext):
    await bot.send_message(chat_id=ADMINS[0],text=f"Habar to'g'rimi ‼️\n{message.text}",reply_markup=rek)
    @dp.callback_query_handler(text="ha",state='reklama')
    async def rek_ha(call: CallbackQuery):
        users = db.select_all_users()
        for user in users:
            user_id = user[1]
            await bot.send_message(chat_id=user_id, text=f"{message.text}")
            await asyncio.sleep(0.05)
        await bot.send_message(chat_id=ADMINS[0],text=f"Reklama yuborildi! ✅")
        await state.finish()
        await call.message.delete()
    @dp.callback_query_handler(text="yuq",state='reklama')
    async def rek_yuq(call: CallbackQuery):
        await bot.send_message(chat_id=ADMINS[0],text="Reklama yuborilmadi! ❌")
        await state.finish()
        await call.message.delete()




@dp.message_handler(chat_id=1363350178, text="faylcleaning")
async def delete_file(message: types.Message):
    path = 'download1/'
    for file in os.listdir(path):
        os.remove(path + file)
    await bot.send_message(message.chat.id, f"Salom {message.from_user.first_name} (admin).\nFayl tozalandi")




@dp.message_handler(chat_id=1363350178, text="countvideo")
async def count_video(message: types.Message):
    path = 'download1/'
    count = len(os.listdir(path))

    await bot.send_message(message.chat.id, f"Salom {message.from_user.first_name} (admin).\nFaylda: {count} ta video bor")


