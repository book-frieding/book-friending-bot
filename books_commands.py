from aiogram import types
from connector import dp, db, book_info
from states import WaitFor
from keyboard import *
from aiogram.types.message import ContentType

from search import search_books
from vector_operations import vectorize_user_by_book


@dp.message_handler(commands=['add_book'], state=WaitFor.free_state)
async def add_book(message: types.Message):
    await message.reply("Please, write the name of the book you want to add as your favorite")
    await WaitFor.waiting_for_book_query.set()


@dp.message_handler(commands=['add_book_by_title'], state=WaitFor.free_state)
async def add_book_by_title(message: types.Message):
    await message.reply("Please, write the name of the book you want to add as your favorite:")
    await WaitFor.waiting_for_book_name_query.set()


@dp.message_handler(commands=['add_book_by_author'], state=WaitFor.free_state)
async def process_start_command(message: types.Message):
    await message.reply("Please, write the name of the author you want to add as your favorite one:")
    await WaitFor.waiting_for_book_author_query.set()


@dp.message_handler(content_types=ContentType.TEXT, state=[WaitFor.waiting_for_book_name_query,
                                                           WaitFor.waiting_for_book_author_query])
async def unknown_message(msg: types.Message):
    book_string = msg.text
    books = await search_books(book_string)
    if len(books) > 0:
        keyboard = await create_keyboard_for_books(["/cannot_find_my_book"] + [b[0] for b in books])
        book_info[msg.from_user.id] = tuple(books)
        await msg.reply("Thanks! \nNow please choose the book you want to add from the list below.",
                        reply_markup=keyboard)
        await WaitFor.waiting_for_book_name.set()
    else:
        await msg.reply("Could not find the book by your query. Please, try another with /add_book command.",
                        reply_markup=kb_help_and_change_contact_info_and_add_book)
        await WaitFor.free_state.set()


@dp.message_handler(commands=['cannot_find_my_book'], state=WaitFor.waiting_for_book_name)
async def unknown_message(msg: types.Message):
    del book_info[msg.from_user.id]
    await msg.reply("That's a pity! Please, try another with /add_book command or you can upload another famous book"
                    " that you like by /add_new_book command.",
                    reply_markup=kb_help_and_change_contact_info_and_add_book)
    await WaitFor.free_state.set()


@dp.message_handler(content_types=ContentType.TEXT, state=WaitFor.waiting_for_book_name)
async def add_existing_book(msg: types.Message):
    book_name_author = msg.text
    book_id = [b[1] for b in book_info[msg.from_user.id] if b[0].strip() == book_name_author.strip()][0]

    document = await db.tg_users.find_one({'_id': {'$eq': msg.from_user.id}})
    if "liked_books_ids" in document:
        books_ids = document["liked_books_ids"]
        books_ids.append(book_id)
        result = await db.tg_users.update_one({'_id': msg.from_user.id}, {'$set': {'liked_books_ids': books_ids}})
    else:
        result = await db.tg_users.update_one({'_id': msg.from_user.id}, {'$set': {'liked_books_ids': [book_id]}})
    del book_info[msg.from_user.id]

    await vectorize_user_by_book(msg.from_user.id)

    await msg.reply("Successfully done! Now you can choose another book or try to find "
                    "new friends based on the book you like!",
                    reply_markup=kb_help_and_change_contact_info_and_add_book_and_find_friend)
    await WaitFor.free_state.set()
