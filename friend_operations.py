from aiogram import types
from connector import dp, db, matches_info
from states import WaitFor
from tree_operations import query_top_k_by_book, book_index
from keyboard import *
from aiogram.types.message import ContentType
from search import search_users


@dp.message_handler(commands=['find_friend'], state="*")
async def find_friends_by_books(msg: types.Message):
    user = await db.tg_users.find_one({'_id': {'$eq': msg.from_user.id}})
    matches = query_top_k_by_book(book_index, user['book_vector'])

    matches = await search_users(matches)
    keyboard = await create_keyboard_for_matches(matches.keys())

    matches_info[user["_id"]] = ((key, matches[key]) for key in matches.keys())

    await msg.reply("Wow! Your possible friends based on your book taste and sorted by similarity with you are below! "
                    "You need to click on the one you are interested in to get the alias and start making friends :)",
                    reply_markup=keyboard)
    await WaitFor.waiting_for_alias.set()


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_alias)
async def add_existing_book(msg: types.Message):
    query_name = msg.text
    query_alias = [m[1] for m in matches_info[msg.from_user.id] if m[0] == query_name][0]
    del matches_info[msg.from_user.id]
    await msg.reply("Alias of chosen user is @{}. Good luck!".format(query_alias),
                    reply_markup=kb_help_and_change_contact_info_and_add_book_and_find_friend)
    await WaitFor.free_state.set()

