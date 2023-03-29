#!/usr/bin/env python3
import io
from collections import Counter
from xml import sax
from xml.sax.handler import ContentHandler

MYTAGS = ["title", "abstract"]


class AbstractWikiHandler(ContentHandler):
    "Handle Wikipedia Abstract's SAX events"
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
                w.strip(r'"/|\()[],.;: ><?!-*')
                for w in value.lower().split()
                if (len(w) > 2 and "=" not in w and "|" not in w)
            )

    def dump(self, file):
        "dump counter to pickle format"
        for k in self.counter.keys():
            file.write(k)
            file.write("\n")


if __name__ == "__main__":
    import sys
    import gzip

    h = AbstractWikiHandler()
    with gzip.open(sys.argv[1], "r") as f:
        sax.parse(f, h)
    print(h.counter.most_common(128))
    print(h.counter.total())
    with open("en.txt", "w", encoding="utf8") as f:
        h.dump(f)
