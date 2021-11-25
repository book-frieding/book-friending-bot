from connector import db
import asyncio


async def search(search_string: str):
    book_cursor = db.books.find({'$text': {'$search': search_string}}, {"score": {"$meta": "textScore"}})  #
    book_cursor.sort([('score', {'$meta': 'textScore'})])
    books = []
    async for book in book_cursor:
        books.append((book['title']+", "+book['author'], book['_id']))
    return books
