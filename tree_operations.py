import asyncio
from annoy import AnnoyIndex
import numpy as np
from connector import db

## 227 and 768


async def build_book_index():
    t = AnnoyIndex(768, 'angular')
    users = db.tg_users.find({})
    vecs = []
    async for user in users:
        if "book_vector" in user.keys():
            vecs.append((int(user["_id"]), user["book_vector"]))
            #t.add_item(int(user["_id"]), (user["book_vector"]))
    for v in vecs:
        t.add_item(v[0], v[1])
        print("!")
    return t


# def build_genre_index(dim, dist, tree_name, vectors=None):
#     t = AnnoyIndex(dim, dist)
#     if vectors is not None:
#         for i, v in vectors:
#             t.add_item(i, v)
#     t.build(10)  # 10 trees
#     t.save(tree_name+'.ann')
#     return t

