from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


button_help = KeyboardButton('/help')
button_tell = KeyboardButton('/tell_about_me')
button_change_contact_info = KeyboardButton('/change_contact_info')
button_change_name = KeyboardButton('/change_name')
button_change_age = KeyboardButton('/change_age')
button_change_gender = KeyboardButton('/change_gender')
button_change_city = KeyboardButton('/change_city')
button_add_book_by_title = KeyboardButton('/add_book_by_title')
button_add_book_by_author = KeyboardButton('/add_book_by_author')
button_find_friend = KeyboardButton('/find_friend')


kb_help = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_help)

kb_tell_and_help = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_tell).add(button_help)

kb_help_and_change_contact_info = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_change_contact_info).add(button_help)

kb_help_and_change_contact_info_and_add_book = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True

).add(button_add_book_by_title).add(button_add_book_by_author).add(button_change_contact_info).add(button_help)

kb_help_and_change_contact_info_and_add_book_and_find_friend = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_find_friend).add(button_add_book_by_title).add(button_add_book_by_author).add(button_change_contact_info).add(button_help)


async def create_keyboard_for_books(book_list):

    book_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    async for book in AsyncIterator(book_list):
        book_button = KeyboardButton(book)
        book_keyboard.add(book_button)

    return book_keyboard

 

async def create_keyboard_for_matches(match_list):

    match_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    async for book in AsyncIterator(match_list):
        book_button = KeyboardButton(book)
        match_keyboard.add(book_button)

    return match_keyboard
