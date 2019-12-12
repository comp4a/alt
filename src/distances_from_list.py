import sys
import pickle
from distences.pd_lev_str import get_distances as lev, get_words_with_max_distance as lev_with_max
from distences.pd_dam_str import get_distances as dam, get_words_with_max_distance as dam_with_max


if __name__=="__main__":
    dist = 0
    if len(sys.argv) > 2:
        listdir = sys.argv[1]
        word = sys.argv[2]
        if len(sys.argv) > 3:
            dist = int(sys.argv[3])
    else:
        print("Sintaxis incorrecta, caraculo")
        sys.exit()

    with open(listdir, "rb") as fh:
        l = pickle.load(fh)
    if not dist:
        print(lev(l, word))
        print(dam(l, word))
    else:
        dl = lev_with_max(l, word, dist)
        dd = dam_with_max(l, word, dist)
        msgl = "{}\t{}\t".format(word, len(dl))
        msgd = "{}\t{}\t".format(word, len(dd))
        for d, w in dl:
            msgl += " " + w
        print(msgl)
        for d, w in dd:
            msgd += " " + w
        print(msgd)