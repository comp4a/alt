import sys
import pickle
from distences.pd_lev_str import get_distances, get_words_with_min_distance


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
        print(get_distances(l, word))
    else:
        dl = get_words_with_min_distance(l, word, dist)
        msg = "{}\t{}\t".format(word, len(dl))
        for d, w in dl:
            msg += " " + w
        print(msg)