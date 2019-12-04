import numpy as np

def levenshtein_distance2(x, y):
    current_row = np.zeros((1+len(x)))
    previous_row = np.zeros((1+len(x)))
    
    current_row[0] = 0
    for i in range(1, len(x)+1):
        current_row[i] = current_row[i-1] + 1
    for j in range(1, len(y)+1):
        previous_row, current_row = current_row, previous_row
        current_row[0] = previous_row[0] + 1
        for i in range(1, len(x)+1):
            current_row[i] = min(current_row[i-1] + 1,
            previous_row[i] + 1,
            previous_row[i-1] + (x[i-1] != y[j-1]))
    return current_row[len(x)]

def distances(index,word):
    word_list = index.keys()
    distance_list = []
    for i,word2 in enumerate(word_list):
        distance = levenshtein_distance2(word2,word)
        distance_list.append( (word2,distance) )

    return distance_list

index = {"patata":[1,2,3],
         "patatero":[1,2,3],
         "patan":[1,2,3]}

print(distances(index,"patata"))

def trie_distances(trie, word):
    res = {}
    
    
