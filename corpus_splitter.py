#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Übung 4 Aufgabe 1.2
# Jana Hofmann, Lucas Seiler

from typing import BinaryIO, Iterable
import gzip
import lxml.etree as ET
import random


def iter_abstract(infile: BinaryIO) -> Iterable:
    """
    Creates an iterable that contains only abstracts (concatenated sentences) of an xml file.
    """
    for _, article in ET.iterparse(infile, tag='section'):
        if article.attrib["type"] == "Abstract":
            abstract = " ".join(sentence.text for sentence in article)
            yield abstract
            article.clear()


def split_corpus(infile: BinaryIO, targetdir: str, n: int = 1000):
    """
    Creates a randomized test, development and training set containing what is inside the input file, each in a
    compressed file.
    The sets are randomized by using two Algorithm R.
    THe first algorithm R fills the container for the test set. Elements which are not added to the test set
    or are removed from it are then considered for the development set. THe second algorithm R fills the container
    for the development set. If they are not added to the development set or are removed from it, they are put into
    the training set. To save RAM, abstracts are written right away to the training set (instead of being
    saved in a container).

    :param infile: opened file in binary mode
    :param targetdir: output directory for files
    :param n: size of test and and development files
    """
    out_dir_training = targetdir + "/abstracts.training.txt.gz"
    out_dir_test = targetdir + "/abstracts.test.txt.gz"
    out_dir_dev = targetdir + "/abstracts.development.txt.gz"
    abstracts = iter_abstract(infile)

    test_reservoir = []
    dev_reservoir = []
    dev_counter = 0  # for second algorithm R
    with gzip.open(out_dir_training, 'wt', encoding='utf8') as trainings_outfile:
        for t, item in enumerate(abstracts):
            dev_item = None  # variable for the unused items of the first algorithm R
            training_item = None  # variable for the unused items of the second algorithm R
            if t < n:
                test_reservoir.append(item)
            else:
                m = random.randint(0, t)
                if m < n:
                    dev_item = test_reservoir[m]  # save item that is to be removed from test_reservoir
                    test_reservoir[m] = item
                else:
                    dev_item = item  # save the skipped item of the first algorithm R

            if dev_item:  # second algorithm R begins if item is not added to test_reservoir or item is removed
                if dev_counter < n:
                    dev_reservoir.append(dev_item)
                else:
                    m = random.randint(0, dev_counter)
                    if m < n:
                        training_item = dev_reservoir[m]  # save item that is to be removed from test_reservoir
                        dev_reservoir[m] = dev_item
                    else:
                        training_item = dev_item  # save the skipped item of the first algorithm R
                dev_counter += 1  # equivalent to t of the dev_algorithm R, increases only if second algorithm R is
                # actually used
            if training_item:  # in case item is not used in or removed from either container, it is added to the
                # training file
                trainings_outfile.write(training_item + "\n")

    with gzip.open(out_dir_test, 'wt', encoding='utf8') as test_outfile, \
            gzip.open(out_dir_dev, 'wt', encoding='utf8') as dev_outfile:
        for abstract in test_reservoir:
            test_outfile.write(abstract + "\n")
        for abstract in dev_reservoir:
            dev_outfile.write(abstract + "\n")


def main():
    file = open("Korpusdaten/abstracts.xml", "rb")
    split_corpus(file, "Korpusdaten")


if __name__ == "__main__":
    main()
