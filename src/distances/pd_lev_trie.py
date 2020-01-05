import numpy as np
from trie import Trie


def get_levenshtein_distances(x: str, trie: Trie, dist_max:int = 999):
    root = trie.root
    root_id = root.node_id
    current_rows = {}
    prefixes = {}
    distances = {}

    first_current_row = np.zeros(len(x) + 1)
    for i in range(1, len(x) + 1):
        first_current_row[i] = first_current_row[i - 1] + 1
    current_rows[root_id] = first_current_row
    prefixes[root_id] = ""

    opened = list(root.children.values())
    while opened:
        me = opened[0]
        for child in me.children.values():
            opened.append(child)
        my_id = me.node_id
        my_char = me.char
        my_father_id = me.father.node_id
        y = prefixes[my_father_id] + my_char
        my_current_row = np.zeros(len(x) + 1)
        my_previous_row = current_rows[my_father_id].copy()
        my_current_row[0] = my_previous_row[0] + 1
        for i in range(1, len(x) + 1):
            my_current_row[i] = min(my_current_row[i - 1] + 1,
                                    my_previous_row[i] + 1,
                                    my_previous_row[i - 1] + (x[i - 1] != my_char))

        prefixes[my_id] = y
        current_rows[my_id] = my_current_row
        if me.end_state:
            dist = my_current_row[len(x)]
            if dist <= dist_max:
                distances[y] = dist
        opened.remove(me)
    return {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
