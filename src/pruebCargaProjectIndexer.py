import sys
import pickle

if __name__=="__main__":
    if len(sys.argv) > 1:
        indexdir = sys.argv[1]

    with open(indexdir, "rb") as fh:
        t = pickle.load(fh)
    print("index_news2docid: {}".format(t[0]))
    print("index_docid2path: {}".format(t[1]))
    print("index_term2news:\n{}".format(t[2]))
    print("index_permuterm:\n{}".format(t[3]))
    print("index_titleterm2news:\n{}".format(t[4]))
    print("index_date2news: {}".format(t[5]))
    print("index_keyword2news:\n{}".format(t[6]))
