import logging
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text
import instaloader
from instaloader import Post
import os
from loader import dp, db, bot
from keyboards.inline.inlinekey import til
from data.config import ADMINS

from aiogram import Bot, Dispatcher, executor,types

@dp.message_handler(Text(startswith='https://www.instagram.com/'))
async def sendvideo(message: types.Message):
    chat_id = message.from_user.id
    user = db.select_user(chat_id=chat_id)
    if user[4] == None:
        await message.answer(f"🇺🇿 Tilni tanlang\n🇺🇸 Select a language\n🇷🇺 Выберите язык", reply_markup=til)
    else:
        try:
            url = message.text

            if len(url) == 63:
                shorted_url = url[31:len(url) - 21]
            elif len(url) == 60:
                shorted_url = url[28:len(url) - 21]
            elif len(url) == 61:
                shorted_url = url[29:len(url) - 21]
            elif len(url) == 71:
                shorted_url = url[31:len(url) - 29]
            else:
                pass
            


            if user[4] == 'uz':
                t = await message.reply('yuklanmoqda...')
            elif user[4] == 'en':
                t = await message.reply('loading...')
            elif user[4] == 'ru':
                t = await message.reply('загрузка...')

            print(shorted_url)
            i = instaloader.Instaloader()
            # i.login('@te', 'Te')
            post = Post.from_shortcode(i.context, shorted_url)
            fil = str(post.date)[0:10] + '_' + str(post.date)[11:13] + '-' + str(post.date)[14:16] + '-' + str(post.date)[17:19] + '_UTC.mp4'
            i.download_post(post, target='download1')
            try:
                video = open("download1/" + fil, "rb")
                await bot.send_video(message.chat.id, video=video,caption="\n@insta1savebot")
                await bot.send_message(chat_id=ADMINS[0],text=f"{message.from_user.first_name} ga video yuborildi..\n{url}")
                path = 'download1/'
                for file in os.listdir(path):
                    if not file.endswith(".mp4"):
                        os.remove(path + file)
            except Exception as e:
                #print(e)
                if user[4] == 'uz':
                    await message.reply('video topilmadi.1')
                elif user[4] == 'en':
                    await message.reply('video not found.1')
                elif user[4] == 'ru':
                    await message.reply('видео не найдено.1')

        except Exception as e:
            #print(e)
            if user[4] == 'uz':
                await message.reply('video topilmadi.2')
            elif user[4] == 'en':
                await message.reply('video not found.2')
            elif user[4] == 'ru':
                await message.reply('видео не найдено.2')

        await t.delete()

