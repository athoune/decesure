"""
Guess if there is an hyphenation between to words.
"""
import gzip


class Decesure:
    "Decesure use a lexicon to un-hyphen words"

    def __init__(self, path: str):
        if path.endswith(".gz"):
            f = gzip.open(path, "r").read().decode("utf-8")
        else:
            f = open(path, "r", encoding="utf8").read()
        self._data = set(f.split("\n"))

    def unhyphen(self, word1: str, word2: str) -> str:
        "Guess if two words are hyphenated"
        word1 = word1.rstrip("-")
        unic = word1 + word2
        multic = "-".join((word1, word2))
        if unic.lower() in self._data:
            return unic
        if multic.lower() in self._data:
            return multic
        if word1.lower() in self._data and word2.lower() in self._data:
            return multic
        return unic


if __name__ == "__main__":
    import sys
    import time

    t1 = time.monotonic_ns()
    cesure = Decesure(sys.argv[1])
    t2 = time.monotonic_ns()
    for k in cesure._data:
        if "-" in k:
            print(k)
    print(
        "Reading the lexicon in", (t2 - t1) / 1000000, "ms", len(cesure._data), "words"
    )
    print(cesure.unhyphen(sys.argv[2], sys.argv[3]))
