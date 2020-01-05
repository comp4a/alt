#! -*- encoding: utf8 -*-
"""
Alumnos:
	Miguel Edo Goterris

	Luis Serrano Hernández
	Risheng Ye

Descripción:
     Recibe una lista de palabras y genera un trie con ellas
     y lo guarda en un archivo
"""
import unicodedata
import time
import re
import pickle
import sys
from trie import Trie

clean_re = re.compile('\W+')


def strip_accents(text):
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)


def clean_text(text):
    text = clean_re.sub(' ', text)
    text = strip_accents(text)
    return text.lower()


def split_text(text):
    text = clean_text(text)
    # Consideraremos separadores de términos los espacios, los saltos de línea y los tabuladores
    return [i for i in re.split(' |\n|\t', text) if i]


def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)


def trie_indexation(docdir: str):
    trie = Trie()
    with open(docdir, 'r') as fh:
        text = fh.read()
        words = split_text(text)
        for word in words:
            trie.add(word)
    return trie


if __name__ == '__main__':
    if len(sys.argv) > 2:
        docdir = sys.argv[1]
        indexdir = sys.argv[2]
    else:
        print("Incorrect use of syntax")

    start = time.time()
    t = trie_indexation(docdir)
    finish = time.time()
    save_object(t, indexdir)

    print(t)
    print("Time: ", finish - start)
