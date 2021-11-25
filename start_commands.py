from aiogram import types
from connector import dp
from states import WaitFor
from keyboard import *
from aiogram.types.message import ContentType
from tree_operations import build_book_index


@dp.message_handler(commands=['start', 'restart'], state="*")
async def process_start_command(message: types.Message):
    await message.reply("Hi! This bot is aimed to help you find friends based on your book tastes!\nBut first of all, "
                        "let's get to know more about you. For introducing yourself, please push "
                        "/tell_about_me button!", reply_markup=kb_tell_and_help)
    await WaitFor.waiting_for_knowing.set()


@dp.message_handler(commands=['tell_about_me'], state=WaitFor.waiting_for_knowing)
async def process_start_command(message: types.Message):
    await message.reply("I will ask you several basic questions about you. "
                        "Please, be honest as it will help other members to "
                        "know how to to contact you. \nFirst of all, what is your name?", reply_markup=kb_help)
    await WaitFor.waiting_for_name.set()