from aiogram import types, Dispatcher
from connector import dp, db, book_info, bot, book_collection
from states import WaitFor
from keyboard import *
from aiogram.types.message import ContentType
from search import search_books
from vector_operations import vectorize_user_by_book
from aiogram_forms import forms
from tree_operations import add_user_to_tree, book_index

from .fields import StringField, ArrayField
from aiogram.dispatcher import FSMContext
from .embeddings import process_description


class BookForm(forms.Form):
    title = StringField('Title')
    author = StringField('Author')
    genres = ArrayField('Genres')
    description = StringField('Description')

    @classmethod
    async def _handle_input(cls, message: types.Message, state: FSMContext) -> None:
        """
        Handle form states messages
        :param message: Chat message
        :param state: FSM context
        :return:
        """
        field = await cls.get_current_field()
        if await field.validate(message.text):
            await state.update_data(**{field.data_key: field.process_message(message.text)})
        else:
            dispatcher = Dispatcher.get_current()
            await dispatcher.bot.send_message(
                types.Chat.get_current().id,
                text="Please, write a {} of the book you want to add:".format(field.validation_error)
            )
            return

        next_field_index = cls._fields.index(field) + 1
        if next_field_index < len(cls._fields):
            await cls._start_field_promotion(cls._fields[next_field_index])
        else:
            await cls.finish(message)

    @classmethod
    async def finish(cls, message) -> None:
        """
        Finish form processing
        :return:
        """
        state = Dispatcher.get_current().current_state()
        await state.reset_state(with_data=False)
        if cls._callback:
            await cls._callback(message)


@dp.message_handler(commands=['add_new_book'], state=WaitFor.free_state)
async def add_new_book(message: types.Message):
    await BookForm.start(callback=_show_info)


async def _show_info(message):
    chat_id = types.Chat.get_current().id
    user_id = message.from_user.id

    print(user_id)

    data = await BookForm.get_data()
    data = data.copy()
    data = {k.lower().split(':')[-1]: v for k, v in data.items()}

    data['book_vector'] = process_description(data['description'])

    insert_one = await db.books.insert_one(data)
    book_id = insert_one.inserted_id
    #
    user = await db.tg_users.find_one({'_id': {'$eq': user_id}})
    books_ids = user.get('liked_books_ids', [])
    books_ids.append(book_id)
    #
    await db.tg_users.update_one({'_id': user_id}, {'$set': {'liked_books_ids': books_ids}})

    await bot.send_message(chat_id, 'Thanks! New book created and added to your favourites!',
                           reply_markup=kb_help_and_change_contact_info_and_add_book_and_find_friend)

    vec = await vectorize_user_by_book(user_id)
    add_user_to_tree(book_index, vec, user_id)
    print("Success")
    await WaitFor.free_state.set()
