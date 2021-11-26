from connector import db
import numpy as np


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


