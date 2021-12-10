from aiogram import types
from connector import dp
from states import WaitFor
from keyboard import *
from aiogram.types.message import ContentType


@dp.message_handler(commands=['help'], state=WaitFor.waiting_for_knowing)
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write your name.",
                        reply_markup=kb_help)


@dp.message_handler(commands=['help'], state=WaitFor.waiting_for_name)
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write your name.",
                        reply_markup=kb_help)


@dp.message_handler(commands=['help'], state=WaitFor.waiting_for_age)
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write your age.",
                        reply_markup=kb_help)


@dp.message_handler(commands=['help'], state=WaitFor.waiting_for_city)
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write your city.",
                        reply_markup=kb_help)


@dp.message_handler(commands=['help'], state=WaitFor.waiting_for_gender)
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write your gender.",
                        reply_markup=kb_help)




@dp.message_handler(commands=['help'], state=[WaitFor.waiting_for_book_name_query,
                                                           WaitFor.waiting_for_book_author_query])
async def process_help_command(message: types.Message):
    await message.reply("Now you need to write the name of the books that you like.",
                        reply_markup=kb_help)
