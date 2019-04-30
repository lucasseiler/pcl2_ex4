#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Übung 4 Aufgabe 1.1
# Jana Hofmann, Lucas Seiler

from typing import BinaryIO, Iterable
import json
import bz2
import gzip
import re


def create_bz2_iterable(infile: BinaryIO) -> Iterable:
    """
    Creates an iterable from a BinaryIO
    """
    with bz2.open(infile) as file:
        for line in file:
            read_line = line
            json_line = read_line.decode("utf-8")
            comment = json.loads(json_line)
            yield comment


def mk_meme_corpus(infile: BinaryIO, outfile: str, min_score: int = 100, min_len: int = 1, max_len: int = 50):
    """
    Creates a compressed corpus of unique comments from a file compressed file (bz2) with json objects.
    The comments are filtered according to certain criteria.
    """
    with bz2.open(infile) as file, gzip.open(outfile, 'wt', encoding='utf8') as outfile:
        comments = (json.loads(line.decode("utf-8")) for line in file)
        # alternative: use function create_bz2_iterable instead of generator expression
        sentence_hashes = set()
        for comment in comments:
            sentence = comment["body"]

            try:  # regex is necessary to remove blank lines in output file caused by whitespace characters
                #  str.strip() has proven to be not entirely effective in removing unnecessary whiespace characters
                sentence = re.search(r'\S.*\S', sentence).group()
            except AttributeError:  # necessary in case there is no match and an attribute error is raised
                continue

            score = comment["score"]
            sentence_length = len(sentence)
            sentence_hash = hash(sentence)

            if sentence_hash not in sentence_hashes and score >= min_score and min_len <= sentence_length <= max_len:
                sentence_hashes.add(sentence_hash)
                outfile.write(sentence)
                print(sentence)


def main():
    file = open("Korpusdaten/RC_2012-06.bz2", "rb")
    mk_meme_corpus(file, "unique_sent.txt.gz", 5, 10, 30)


if __name__ == "__main__":
    main()


