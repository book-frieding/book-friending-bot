from aiogram.dispatcher.filters.state import State, StatesGroup


class WaitFor(StatesGroup):
    waiting_for_knowing = State()
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_city = State()
    waiting_for_gender = State()
    waiting_for_book_query = State()
    waiting_for_book_name = State()

    waiting_for_book_upload = State()

    changing_contact_info = State()
    free_state = State()
