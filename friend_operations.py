from aiogram import types
from connector import dp, db, book_info
from states import WaitFor
from tree_operations import query_top_k_by_book, book_index
from keyboard import *
from aiogram.types.message import ContentType
from search import search
from vector_operations import vectorize_user_by_book, vectorize_user_by_genre


@dp.message_handler(commands=['find_friend_by_books'], state="*")
async def find_friend_by_books(msg: types.Message):
    user = await db.tg_users.find_one({'_id': {'$eq': msg.from_user.id}})
    matches = query_top_k_by_book(book_index, user['book_vector'])
    match_1 = await db.tg_users.find_one({'_id': {'$eq': int(matches[0])}})
    match_2 = await db.tg_users.find_one({'_id': {'$eq': int(matches[1])}})
    match_3 = await db.tg_users.find_one({'_id': {'$eq': int(matches[2])}})
    await msg.reply("Wow! Your possible friends based on the books you like could be @{}, @{}, @{}!"
                    .format(match_1["username"], match_2["username"], match_3["username"]))
    await WaitFor.free_state.set()

@dp.message_handler(commands=['find_friend_by_author'], state="*")
async def find_friend_by_author(msg: types.Message):
    user = await db.tg_users.find_one({'_id': {'$eq': msg.from_user.id}})
    matches = query_top_k_by_book(book_index, user['book_vector'])
    match_1 = await db.tg_users.find_one({'_id': {'$eq': int(matches[0])}})
    match_2 = await db.tg_users.find_one({'_id': {'$eq': int(matches[1])}})
    match_3 = await db.tg_users.find_one({'_id': {'$eq': int(matches[2])}})
    await msg.reply("Wow! Your possible friends based on the books you like could be @{}, @{}, @{}!"
                    .format(match_1["username"], match_2["username"], match_3["username"]))
    await WaitFor.free_state.set()

@dp.message_handler(commands=['find_friend_genre'], state="*")
async def find_friend_by_genre(msg: types.Message):
    user = await db.tg_users.find_one({'_id': {'$eq': msg.from_user.id}})
    matches = query_top_k_by_book(book_index, user['book_vector'])
    match_1 = await db.tg_users.find_one({'_id': {'$eq': int(matches[0])}})
    match_2 = await db.tg_users.find_one({'_id': {'$eq': int(matches[1])}})
    match_3 = await db.tg_users.find_one({'_id': {'$eq': int(matches[2])}})
    await msg.reply("Wow! Your possible friends based on the books you like could be @{}, @{}, @{}!"
                    .format(match_1["username"], match_2["username"], match_3["username"]))
    await WaitFor.free_state.set()
