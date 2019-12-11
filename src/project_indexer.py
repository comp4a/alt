#! -*- encoding: utf8 -*-
"""
Alumnos:
	Miguel Edo Goterris
	Andrey Kramer Savelev
	Luis Serrano Hernández
	Risheng Ye

Ampliaciones hechas:
	permuterms
	indices adicionales
	busqueda de varios terminos consecutivos
	parentesis
"""

import re
import sys
import pickle
import os
import json
# insort permite insertar elementos de forma ordenada partiendo de una lista que ya lo está
from bisect import insort
from unicodedata import normalize

clean_re = re.compile('\W+')
def clean_text(text):
    # Se quitan caracteres de puntuación
    text = clean_re.sub(' ', text)
    # Se quitan los acentos, dieresis etc.
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    text = normalize('NFKC', normalize('NFKD', text).translate(trans_tab))
    # Se pasa a minúsculas
    return text.lower()

def split_text(text):
    # Consideraremos separadores de términos los espacios, los saltos de línea y los tabuladores
    return [i for i in re.split(' |\n|\t',text) if i]
    
def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj

def index_term(term, newsid, position, index_term2news, index_permuterm):
    newsdic = index_term2news.get(term)
    # Si no hay noticias registradas para el término
    if not newsdic:
        # Se obtienen sus permutaciones
        permuterm_indexer(term, index_permuterm)
        index_term2news[term] = {newsid:[position]}
    # Si ya hay noticias registradas para el término
    else:
        if newsid in newsdic.keys():
            poslist = newsdic[newsid]
            poslist.append(position)
            newsdic[newsid] = poslist
        else:
            newsdic[newsid] = [position]
        index_term2news[term] = newsdic

def index_titleterm(term, newsid, index_titleterm2news):
    # Si el término es nuevo se obtienen sus permutaciones
    newslist = index_titleterm2news.get(term)
    if not newslist:
        index_titleterm2news[term] = [newsid]
    # Si ya hay noticias registradas para el término
    else:
        newslist.append(newsid)
        index_titleterm2news[term] = newslist

def index_keyword(keyword, newsid, index_keyword2news):
    keywordlist = index_keyword2news.get(keyword)
    # Si la categoría es nueva
    if not keywordlist:
        index_keyword2news[keyword] = [newsid]
    # Si ya existían noticias con esta categoría
    else:
        keywordlist.append(newsid)
        index_keyword2news[keyword] = keywordlist

def index_date(date, newsid, index_date2news):
    datelist = index_date2news.get(date) 
    # Si la fecha es nueva
    if not datelist:
        index_date2news[date] = [newsid]
    # Si ya existían noticias con esta fecha
    else:
        datelist.append(newsid)
        index_date2news[date] = datelist

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
    index_term2news = {}
    # Lista de de permutaciones. Cada permutación apunta a los términos de los que puede provenir.
    # Puede haber tuplas con la misma permutación, pero tendrán distinto término.
    index_permuterm = []
    # Diccionario : date -> newsid
    index_date2news = {}
    # Diccionario : keywords -> newsid
    index_keyword2news = {}
    # Diccionario : titleterm -> newsid
    index_titleterm2news = {}
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
                content = noticia["article"]
                title = noticia["title"]
                categorias = noticia["keywords"]
                date = noticia["date"]
                # Obtención de tokens
                content = clean_text(content)
                content = split_text(content)
                categorias = split_text(clean_text(categorias))
                title = split_text(clean_text(title))
                position = 1                
                # Una iteración por cada término dentro de la noticia
                for term in content:
                    # Indexación del término en el índice de término -> (noticia, posición)
                    index_term(term, newsid, position, index_term2news, index_permuterm)
                    position = position + 1
                # Una iteración por cada término dentro del título de la noticia
                for titleterm in title:
                    # Indexación del término en el índice de términos en títulos
                    index_titleterm(titleterm, newsid,  index_titleterm2news)
                # Una iteración por cada categoría de la noticia
                for keyword in categorias:
                    # Indexación de la categoría
                    index_keyword(keyword, newsid, index_keyword2news)
                # Indexación de la fecha
                index_date(date, newsid, index_date2news)     
                newsid = newsid + 1
                posindoc = posindoc + 1
            docid = docid + 1

    objects2save = (index_news2docid, index_docid2path, index_term2news, index_permuterm, index_titleterm2news,index_date2news,index_keyword2news)
    save_object(objects2save, indexdir)

def permuterm_indexer(term, permutation_list):
    """
    DESCRIPCIÓN:

        Obtiene todas las rotaciones del término y las añade a la lista de rotaciones global. La
        inserción se hace de forma ordenada

    PARAMETROS:

        - term -> Término a permutar

        - permutation_list -> Lista ordenada alfabéticamente de las permutaciones de todos lo
        términos analizados hasat el momento

    NOTA:

        El hecho de que la lista sea ordenada no sólo ayuda a que la búsqueda sea más sencilla
        y eficiente, también permite una inserción ordenada muy rápida
    
    """
    term_aux = term + '$'
    for i in range(0, len(term_aux)):
        permutation = term_aux[i:] + term_aux[:i]
        insort(permutation_list,(permutation, term))

def syntax():
    print("Use the correct syntax:\n\t-First argument:Path of the collection\n\t-Second Argument:Path to save the index")
    sys.exit()
    
if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        docsdir = sys.argv[1]
        indexdir = sys.argv[2]
    else:
        syntax()
    
    doc_walker(docsdir, indexdir)

