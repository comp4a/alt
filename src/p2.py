#! -*- encoding: utf8 -*-
import numpy as np
import sys

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

def compare2list(word, list_of_words):
    for w in list_of_words:
        print(word, " -> ", w , ": ", levenshtein_distance2(word, w))

def syntax():
    print("Use the correct syntax:\n\t-Seconmd argument:Word to comapre\n\t-Seconmd argument:Path of the document")
    sys.exit()
    

if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        word = sys.argv[1]
        indexdir = sys.argv[2]
    else:
        syntax()
    
    with open(indexdir, 'r') as fh:
        list_of_words = fh.read()
        compare2list(word, list_of_words)
        
