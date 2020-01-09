import sys
import pickle
from random import randint
from distences.pd_lev_trie import get_levenshtein_distances as levT
from distences.pd_dam_trie import get_damerau_levenshtein_distances as damT
from distences.pd_lev_str import get_words_with_max_distance as levL
from distences.pd_dam_str import get_words_with_max_distance as damL

if __name__=="__main__":
    palabra = "casa"
    noticia = randint(1, 100)

    if len(sys.argv) > 1:
        indexdir = sys.argv[1]
        if len(sys.argv) > 2:
            noticia = int(sys.argv[2])
            if len(sys.argv) > 3:
                palabra = sys.argv[3]


    print("Cargando índices")
    with open(indexdir, "rb") as fh:
        t = pickle.load(fh)
    index_news2docid = t[0]
    index_docid2path = t[1]
    index_term2news = t[2]
    index_permuterm = t[3]
    index_titleterm2news = t[4]
    index_date2news = t[5]
    index_keyword2news = t[6]
    print("Índices cargados")

    noticia_pos = index_news2docid[noticia]
    print("La noticia {} está en el documento {}, en la posición {}".format(noticia,
        noticia_pos[0],noticia_pos[1]))
    ruta = index_docid2path[noticia_pos[0]]
    print("La ruta del documento es: {}".format(ruta))
    news_list = index_term2news.get(palabra);
    print('La palabra {} se encuentra presente en {}"'.format(palabra, news_list))
    news_list = index_titleterm2news.get(palabra);
    print('La palabra {} se encuentra presente en el título en {}"'.format(palabra, news_list))

    print("Cálculo de distancias")
    print("Distancias con trie")
    print("Levhenstein")
    distsL = levT(palabra, index_term2news, 2)

    msgL = "{}\t{}: ".format(palabra, len(distsL.keys()))
    for w in distsL.keys():
        msgL += "{} ({}), ".format(w, distsL[w])

    print(msgL)

    print("Damerau")
    distsD = damT(palabra, index_term2news, 2)

    msgD = "{}\t{}: ".format(palabra, len(distsD.keys()))
    for w in distsL.keys():
        msgD += "{} ({}), ".format(w, distsD[w])

    print(msgD)

    print("Pasando tries a lista")
    lista = index_term2news.to_list()

    print("Distancias con listas")
    print("Levhenstein")
    distsL = levL(palabra, lista, 2)

    msgL = "\n{}\t{}: ".format(palabra, len(distsL))
    for d, w in distsL:
        msgL += "{} ({}), ".format(w, d)

    print(msgL)

    print("Damerau")
    distsD = damL(palabra, lista, 2)

    msgD = "\n{}\t{}: ".format(palabra, len(distsD))
    for d, w in distsL:
        msgD += "{} ({}), ".format(w, d)

    print(msgD)
