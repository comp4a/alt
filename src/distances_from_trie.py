import sys
import pickle
from distences.pd_lev_trie import get_levenshtein_distances as lev
from distences.pd_dam_trie import get_damerau_levenshtein_distances as dam

if __name__=="__main__":
    dist = -1
    if len(sys.argv) > 2:
        triedir = sys.argv[1]
        word = sys.argv[2]
        if len(sys.argv) > 3:
            dist = int(sys.argv[3])
    else:
        print("Sintaxis incorrecta, caraculo")
        sys.exit()

    with open(triedir, "rb") as fh:
        t = pickle.load(fh)
    if dist < 0:
        resl = lev(word, t)
        rest = dam(word, t)
    else:
        resl = lev(word, t, dist)
        rest = dam(word, t, dist)
    msgl = "{}\t{}\t".format(word, len(resl.keys()))
    msgt = "{}\t{}\t".format(word, len(rest.keys()))
    for w in resl.keys():
        msgl += "{} ".format(w)
    for w in rest.keys():
        msgt += "{} ".format(w)
    print(msgl)
    print(msgt)