from aiogram import types
from connector import dp, db, contact_info, contact_info_mapping
from states import WaitFor
from keyboard import *
from aiogram.types.message import ContentType
import datetime


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_name)
async def unknown_message(msg: types.Message):
    contact_info[msg.from_user.id] = msg.text
    await msg.reply("Thanks! \nNow please write the year of your birth.", reply_markup=kb_help)
    await WaitFor.waiting_for_age.set()


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_age)
async def unknown_message(msg: types.Message):
    try:
        contact_info[msg.from_user.id] = (contact_info[msg.from_user.id], int(msg.text))
        await msg.reply("Thanks! \nNow please write the place where you are currently located", reply_markup=kb_help)
        await WaitFor.waiting_for_city.set()
    except Exception as e:
        await msg.reply("Year of your birth should be integer number. Please, try one more time:", reply_markup=kb_help)


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_city)
async def unknown_message(msg: types.Message):
    contact_info[msg.from_user.id] = (contact_info[msg.from_user.id][0], contact_info[msg.from_user.id][1], msg.text)
    await msg.reply("Thanks! \nNow please write your gender", reply_markup=kb_help)
    await WaitFor.waiting_for_gender.set()


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_gender)
async def unknown_message(msg: types.Message):
    contact_info[msg.from_user.id] = (contact_info[msg.from_user.id][0], contact_info[msg.from_user.id][1],
                                      contact_info[msg.from_user.id][2], msg.text)
    doc = {contact_info_mapping[i]: info for i, info in enumerate(contact_info[msg.from_user.id])}
    doc['_id'] = msg.from_user.id
    doc['username'] = msg.from_user.username
    del contact_info[msg.from_user.id]

    user = await db.tg_users.find_one({'_id': {'$eq':  msg.from_user.id}})
    if user is None:
        result = await db.tg_users.insert_one(doc)
        print('result %s' % repr(result.inserted_id))
    else:
        if "liked_books_ids" in user.keys():
            doc["liked_books_ids"] = user["liked_books_ids"]
            doc["book_vector"] = user["book_vector"]
        result = await db.tg_users.replace_one({'_id': msg.from_user.id}, doc)
        print('replaced %s document' % result.modified_count)

    now = datetime.datetime.now()
    if user is not None and "liked_books_ids" in user.keys():
        keyb = kb_help_and_change_contact_info_and_add_book_and_find_friend
    else:
        keyb = kb_help_and_change_contact_info_and_add_book

    await msg.reply("Thanks! Now we are done with this! Your contact information is:\n \n"
                    "Name: {}\n"
                    "Age: {}\n"
                    "Location: {}\n"
                    "Gender: {}\n\n"
                    "I know more about your personality, but I still need to "
                    "collect some books that you like! \nIf you would like to change your contact information "
                    "you can do it at any time with /change_contact_info button".format(doc["name"],
                                                                                        now.year - doc["age"],
                                                                                        doc["location"], doc["gender"]),
                    reply_markup=keyb)
    await WaitFor.free_state.set()


@dp.message_handler(commands=['change_contact_info'], state=[WaitFor.free_state])
async def process_start_command(message: types.Message):
    await message.reply("Write your name:")
    await WaitFor.waiting_for_name.set()
