from connector import pym_db
import hnswlib
import numpy as np


def create_index(dim=768):
    book_vec = []
    _ids = []
    users = pym_db.tg_users
    for user in users.find({}):
        if "book_vector" in user:
            book_vec.append(np.array(user["book_vector"]))
            _ids.append(int(user["_id"]))

    p = hnswlib.Index(space='cosine', dim=dim)
    p.init_index(max_elements=len(book_vec)*2, ef_construction=200, M=16)
    p.add_items(book_vec, _ids)
    return p


def query_top_k_by_book(p, vector):
    labels, distances = p.knn_query(np.array(vector), k=6)
    return labels[0][1:]


book_index = create_index()


