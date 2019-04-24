#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Übung 4 Aufgabe 2
# Lucas Seiler, Jana Hofmann

from typing import Iterable


def longest_substrings(x: str, y: str) -> Iterable[str]:
    x = x.lower()
    y = y.lower()
    table = [[0 for char in x] for char in y]

    max_length = 0
    max_index_list = []
    row_counter = 0
    for row in table:
        column_counter = 0
        for element in row:
            if x[column_counter] == y[row_counter] and (row_counter == 0 or column_counter == 0):
                table[row_counter][column_counter] += 1
            elif x[column_counter] == y[row_counter]:
                table[row_counter][column_counter] = table[row_counter-1][column_counter-1] + 1
            if table[row_counter][column_counter] > max_length:
                max_length = table[row_counter][column_counter]
                max_index_list = [column_counter]
            elif table[row_counter][column_counter] == max_length:
                # save the index of the last letter of the substring of the x word
                max_index_list.append(column_counter)
            column_counter += 1
        row_counter += 1

    substring_list = [x[index-max_length+1:index+1] for index in max_index_list]
    if not substring_list[0]:
        return "None"
    else:
        return substring_list


print(longest_substrings("Meisterklasse", "Kleistermasse"))
print(longest_substrings('Tod', 'Leben'))
print(longest_substrings('mozart','mozzarella'))
print(longest_substrings('keep the interface!', 'KeEp ThE iNtErFaCe!'))



