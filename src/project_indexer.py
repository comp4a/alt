#! -*- encoding: utf8 -*-
"""
Alumnos:
	Miguel Edo Goterris

	Luis Serrano Hernández
	Risheng Ye

"""

from trie import TrieDict, Trie
from text_cleaner import split_text as clean_text
import sys
import pickle
import os
import json

def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)


def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj


def index_term(term, newsid, position, index_term2news, index_permuterm):
    print(term)
    end_node = index_term2news.reach_node(term, True)
    newsdic = end_node.content
    if newsdic:
        poslist = newsdic.get(newsid, None)
        if poslist:
            newsdic[newsid] = poslist.append(position)
        else:
            newsdic[newsid] = [position]
        end_node.content = newsdic
    else:
        end_node.content = {newsid: [position]}
        permuterm_indexer(term, index_permuterm)


def index_titleterm(term, newsid, index_titleterm2news):
    end_node = index_titleterm2news.reach_node(term, True)
    newslist = end_node.content
    if not newslist:
        end_node.content = [newsid]
    else:
        newslist.append(newsid)
        end_node.content = newslist


def index_keyword(keyword, newsid, index_keyword2news):
    end_node = index_keyword2news.reach_node(keyword)
    newslist = end_node.content
    if newslist:
        newslist.append(newsid)
        end_node.content = newslist
    else:
        end_node.content = [newsid]

def index_date(date, newsid, index_date2news):
    datelist = index_date2news.get(date)
    # Si la fecha es nueva
    if not datelist:
        index_date2news[date] = [newsid]
    # Si ya existían noticias con esta fecha
    else:
        datelist.append(newsid)
        index_date2news[date] = datelist


def permuterm_indexer(term: str, permutation_trie: TrieDict):
    """
    DESCRIPCIÓN:

        Obtiene todas las rotaciones del término y las añade al trie de rotaciones global.

    PARAMETROS:

        - term -> Término a permutar

        - permutation_trie -> Trie containing the permutations an their corresponding original word

    """
    term_aux = term + '$'
    for i in range(0, len(term_aux)):
        permutation = term_aux[i:] + term_aux[:i]
        permutation_trie.add(permutation, term)

def doc_walker(docsdir, indexdir):
    """
    DESCRIPCIÓN:

        Recorre todos los documentos del directorio y genera el índice

    PARAMETROS:

        - docsdir -> Directorio a recorrer

        - indexdir -> Directorio en el que se creará el índice
    
    """
    # Diccionario: docid -> Ubicación del documento
    index_docid2path = {}
    # Diccionario : newsid -> (docid, pos)
    index_news2docid = {}
    # Diccionario : term -> [newsid] -> [pos]
    index_term2news = TrieDict()
    # Lista de de permutaciones. Cada permutación apunta a los términos de los que puede provenir.
    # Puede haber tuplas con la misma permutación, pero tendrán distinto término.
    index_permuterm = TrieDict()
    # Diccionario : date -> newsid
    index_date2news = {}
    # Diccionario : keywords -> newsid
    index_keyword2news = TrieDict()
    # Diccionario : titleterm -> newsid
    index_titleterm2news = TrieDict()
    docid = 1
    newsid = 1
    # Una iteración por cada carpeta en el directorio
    for dirname, subdirs, files in os.walk(docsdir):
        # Una iteración por cada archivo en la carpeta
        for filename in files:
            fullname = os.path.join(dirname, filename)
            noticias = load_json(fullname)
            index_docid2path[docid] = fullname
            posindoc = 1
            # Una iteración por cada noticia dentro del fichero
            for noticia in noticias:
                # Extracción de partes de la noticia
                index_news2docid[newsid] = (docid, posindoc)
                contenido = noticia["article"]
                title = noticia["title"]
                categorias = noticia["keywords"]
                date = noticia["date"]
                # Obtención de tokens
                contenido = clean_text(contenido)
                categorias = clean_text(categorias)
                title = clean_text(title)
                position = 1
                # Una iteración por cada término dentro de la noticia
                for term in contenido:
                    # Indexación del término en el índice de término -> (noticia, posición)
                    index_term(term, newsid, position, index_term2news, index_permuterm)
                    position = position + 1
                # Una iteración por cada término dentro del título de la noticia
                for titleterm in title:
                    # Indexación del término en el índice de términos en títulos
                    index_titleterm(titleterm, newsid, index_titleterm2news)
                # Una iteración por cada categoría de la noticia
                for keyword in categorias:
                    # Indexación de la categoría
                    index_keyword(keyword, newsid, index_keyword2news)
                # Indexación de la fecha
                index_date(date, newsid, index_date2news)
                newsid = newsid + 1
                posindoc = posindoc + 1
            docid = docid + 1

    objects2save = (
        index_news2docid, index_docid2path, index_term2news, index_permuterm,
        index_titleterm2news, index_date2news, index_keyword2news)
    save_object(objects2save, indexdir)

def syntax():
    print(
        "Use the correct syntax:\n\t-First argument:Path of the collection\n\t-Second Argument:Path to save the index")
    sys.exit()


if __name__ == '__main__':

    if len(sys.argv) > 2:
        docsdir = sys.argv[1]
        indexdir = sys.argv[2]
    else:
        syntax()

    doc_walker(docsdir, indexdir)
