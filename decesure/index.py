#!/usr/bin/env python3
import io
from collections import Counter
from xml import sax
from xml.sax.handler import ContentHandler
import pickle

MYTAGS = ["title", "abstract"]


class AbstractWikiHandler(ContentHandler):
    buffer = io.StringIO()
    path = []
    counter = Counter()

    def startElement(self, name, attrs):
        self.path.append(name)
        if name in MYTAGS:
            self.buffer = io.StringIO()

    def characters(self, content):
        if self.path[-1] in MYTAGS:
            self.buffer.write(content)

    def endElement(self, name):
        self.path.pop()
        if name in MYTAGS:
            value = self.buffer.getvalue()
            if name == "title":
                value = value[11:]
            self.counter.update(
                w.strip('"|()[],. <>?!') for w in value.lower().split() if (len(w) > 2)
            )

    def dump(self, file):
        "dump counter to pickle format"
        pickle.dump(dict(self.counter), file)


if __name__ == "__main__":
    import sys
    import gzip

    h = AbstractWikiHandler()
    with gzip.open(sys.argv[1], "r") as f:
        sax.parse(f, h)
    print(h.counter.most_common(128))
    print(h.counter.total())
    h.dump(open("en.pickle", "wb"))
