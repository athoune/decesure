# Décésure

Rebuild hyphenated words, using Wikpedia abstract as a lexicon.

In french, *césure* means *hyphen*, *décésure* is a neologism meaning *unhyphen*.

## Build a lexicon

Go get some abstract.xml.gz file somewhere in http://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/

```bash
python -m decesure.index ~/Downloads/enwiki-20230320-abstract.xml.gz
```

You can compress the lexicon

```bash
gzip -9 en.txt
```

## Use it

```bash
python -m decesure en.txt.gz deploy- ment
```
