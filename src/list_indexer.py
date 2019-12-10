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
"""
import unicodedata
import re
import pickle
import sys
import time
from bisect import insort_left, bisect_left

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


def list_indexation(docdir: str):
    word_list = []
    with open(docdir, 'r') as fh:
        text = fh.read()
        words = split_text(text)
        for word in words:
            index = bisect_left(word_list, word)
            if index > len(word_list) - 1:
                word_list.insert(index, word)
            elif word_list[index] != word:
                word_list.insert(index, word)
    return word_list


if __name__ == '__main__':
    if len(sys.argv) > 2:
        docdir = sys.argv[1]
        indexdir = sys.argv[2]
    else:
        print("Incorrect use of syntax")

    start = time.time()
    l = list_indexation(docdir)
    finish = time.time()
    save_object(l, indexdir)

    print(l)
    print("Time: ", finish - start)
