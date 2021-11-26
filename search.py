from connector import db
import asyncio
import datetime


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


async def search_books(search_string: str):
    book_cursor = db.books.find({'$text': {'$search': search_string}}, {"score": {"$meta": "textScore"}})  #
    book_cursor.sort([('score', {'$meta': 'textScore'})])
    books = []
    async for book in book_cursor:
        books.append((book['title']+", "+book['author'], book['_id']))
    return books


async def search_books(search_string: str):
    book_cursor = db.books.find({'$text': {'$search': search_string}}, {"score": {"$meta": "textScore"}})  #
    book_cursor.sort([('score', {'$meta': 'textScore'})])
    books = []
    async for book in book_cursor:
        books.append((book['title']+", "+book['author'], book['_id']))
    return books


async def search_users(user_ids: list):
    users = []
    async for _id in AsyncIterator(user_ids):
        u = await db.tg_users.find_one({'_id': {'$eq': int(_id)}})
        users.append(u)

    users_output = {}
    now = datetime.datetime.now()

    async for u in AsyncIterator(users):
        users_output[u["name"] + ", " + str(now.year - u["age"]) + "y.o., "+u["location"] + ", " + u["gender"]] \
            = u["username"]

    return users_output
