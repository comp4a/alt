#! -*- encoding: utf8 -*-
"""
Alumnos:
	Miguel Edo Goterris

	Luis Serrano Hernández
	Risheng Ye

"""

import re
import unicodedata

clean_re = re.compile('\W+')


def strip_accents(text):
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)


def clean_text(text):
    text = clean_re.sub(' ', text)
    # text = strip_accents(text)
    return text.lower()


def split_text(text):
    text = clean_text(text)
    # Consideraremos separadores de términos los espacios, los saltos de línea y los tabuladores
    return [i for i in re.split(' |\n|\t', text) if i]