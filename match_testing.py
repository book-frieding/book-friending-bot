from annoy import AnnoyIndex
import numpy as np

GENRES = []


user1_books = [[1, 2, 3], [1, 2, 3]]
user1_genres = ["tale", "fantasy", "detective"]

user2_books = [[1, 5, 3], [1, 9, 3]]
user2_genres = ["tale", "fantasy", "detective"]


def calculate_user_book_vector(user_books):
    book_vector = np.mean(np.array(user_books), axis=1)
    return book_vector


def build_annoy_index(dim, dist, tree_name, vectors=None):
    t = AnnoyIndex(dim, dist)
    if vectors is not None:
        for i, v in vectors:
            t.add_item(i, v)
    t.build(10)  # 10 trees
    t.save(tree_name+'.ann')
    return t


book_tree = build_annoy_index(256, 'angular', 'book_tree')
genre_tree = build_annoy_index(70, 'hamming', 'genre_tree')


def add_item(tree, _id, vector, tree_name):
    tree.add_item(_id, vector)
    tree.save(tree_name + '.ann')


def get_10_matches_with_tree(_id, tree):
    return tree.get_nns_by_item(_id, 11)[1:]


def match_with_set(set1, set2):
    set1 = set(set1)
    set2 = set(set2)
    return len(set1 & set2) / len(set1 | set2)


def get_10_matches_with_set(query, user_pairs): # user_pairs - array of pairs (_id, author_set)
    users = sorted(user_pairs, key=lambda x: match_with_set(query, x[1]), reverse=True)
    return [user[0] for user in users][1:11]


def build_genre_vec(genres):
    vec = []
    for g in GENRES:
        if g in genres:
            vec.append(1)
        else:
            vec.append(0)
    return vec


def build_user(_id, book_vectors, genres):
    genres_vec = build_genre_vec(genres)
    book_vec = calculate_user_book_vector(book_vectors)
    add_item(book_tree, _id, book_vec, 'book_tree')
    add_item(genre_tree, _id, genres_vec, 'genre_tree')




