#! -*- encoding: utf8 -*-
"""
Alumnos:
	Miguel Edo Goterris

	Luis Serrano Hernández
	Risheng Ye

Descripción:
    Genera un archivo indice que alamcena una lista ordenada de
    las palabras que aparecen en el texto. Los caracteres de
    puntuacion y los acentos son eliminados y la coimpletidud del texto
    es tratado como palabras en minusculas
    A partir de la lista anterior genera un trie y lo almacena también
"""
import sys
import unicodedata
import re
import pickle
import time
from bisect import bisect_left
from trie import Trie

clean_re = re.compile('\W+')


def strip_accents(text):
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)


def clean_text(text):
    text = clean_re.sub(' ', text)
    #text = strip_accents(text)
    return text.lower()


def split_text(text):
    text = clean_text(text)
    # Consideraremos separadores de términos los espacios, los saltos de línea y los tabuladores
    return [i for i in re.split(' |\n|\t', text) if i]


def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)


def list_indexation(docdir: str):
    word_list = []
    with open(docdir, 'r') as file:
        text = file.read()
        words = split_text(text)
        for word in words:
            index = bisect_left(word_list, word)
            if index > len(word_list) - 1:
                word_list.insert(index, word)
            elif word_list[index] != word:
                word_list.insert(index, word)
    return word_list


def trie_indexation(index_list: list):
    trie = Trie()
    for word in index_list:
        trie + str(word)
    return trie


if __name__ == "__main__":
    if len(sys.argv) > 3:
        docdir = sys.argv[1]
        listdir = sys.argv[2]
        triedir = sys.argv[3]
    else:
        print("Incorrect use of syntax")
        sys.exit()

    time_start = time.time()
    index_list = list_indexation(docdir)
    time_list_end = time.time()
    index_trie = trie_indexation(index_list)
    time_finish = time.time()

    print("Indexation finished:\nTimes\n-----\nList:\t", time_list_end - time_start\
          , "\nTrie:\t", time_finish - time_list_end, "\nTotal:\t", time_finish -time_start)

    save_object(index_list, listdir)
    save_object(index_trie, triedir)

    dec = input("Do you want to display the list?\n")
    if bool(dec):
        print(index_list)

    dec = input("Do you want to display the trie?\n")
    if bool(dec):
        print(index_trie)

