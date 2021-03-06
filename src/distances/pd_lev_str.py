import numpy as np
from bisect import bisect_left


def levenshtein_distance(x: str, y: str, show_table: bool = False):
    current_row = np.zeros((1 + len(x)))
    previous_row = np.zeros((1 + len(x)))
    for i in range(1, len(x) + 1):
        current_row[i] = current_row[i - 1] + 1

    for j in range(1, len(y) + 1):
        previous_row, current_row = current_row, previous_row
        current_row[0] = previous_row[0] + 1
        for i in range(1, len(x) + 1):
            current_row[i] = min(current_row[i - 1] + 1,
                                 previous_row[i] + 1,
                                 previous_row[i - 1] + (x[i - 1] != y[j - 1]))

    return current_row[len(x)]


def get_distances(word: str, index_list: list):
    distances_list = []
    for w in index_list:
        d = levenshtein_distance(w, word)
        insertion = (d, w)
        index = bisect_left(distances_list, insertion)
        distances_list.insert(index, insertion)
    return distances_list


def get_words_with_max_distance(word: str, index_list: list, dist: int):
    distances_list = []
    for w in index_list:
        d = levenshtein_distance(w, word)
        if d <= dist:
            insertion = (d, w)
            index = bisect_left(distances_list, insertion)
            distances_list.insert(index, insertion)
    return distances_list
