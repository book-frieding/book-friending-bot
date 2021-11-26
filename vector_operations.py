from connector import db
import asyncio
import numpy as np
from genres import genres


async def vectorize_user_by_book(_id):
    vec = []
    user = await db.tg_users.find_one({'_id': {'$eq': _id}})
    book_list = list(user["liked_books_ids"])
    book_cursor = db.books.find({'_id': {'$in': book_list}})  #
    for book in await book_cursor.to_list(length=100):
        vec.append(book['book_vector'])
    vec = np.array(vec)
    vec = list(np.mean(vec, axis=0))
    result = await db.tg_users.update_one({'_id': _id}, {'$set': {'book_vector': vec}})


async def vectorize_user_by_genre(_id):
    vec = []
    user_genres = set()
    user = await db.tg_users.find_one({'_id': {'$eq': _id}})
    book_list = list(user["liked_books_ids"])
    book_cursor = db.books.find({'_id': {'$in': book_list}})  #
    for book in await book_cursor.to_list(length=100):
        for g in (book['genres']):
            user_genres.add(g)
    for g in genres:
        if g in user_genres:
            vec.append(1)
        else:
            vec.append(0)

    result = await db.tg_users.update_one({'_id': _id}, {'$set': {'genre_vector': vec}})
