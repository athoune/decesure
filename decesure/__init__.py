"""
Guess if there is an hyphenation between to words.
"""
import gzip
import pickle


class Cesure:
    def __init__(self, path: str):
        if path.endswith(".gz"):
            f = gzip.open(path, "r")
        else:
            f = open(path, "rb")
        self._data = pickle.load(f)
        f.close()

    def unhyphen(self, word1: str, word2: str) -> str:
        word1 = word1.rstrip("-")
        unic = word1 + word2
        multic = "-".join(word1, word2)
        if unic.lower() in self._data:
            return unic
        if multic.lower() in self._data:
            return multic
        if word1.lower() in self._data and word2.lower() in self._data:
            return multic
        return unic


if __name__ == '__main__':
    import sys
    cesure = Cesure(sys.argv[1])
    for k in cesure._data:
        if "-" in k:
            print(k)
    print(cesure.unhyphen(sys.argv[2], sys.argv[3]))
