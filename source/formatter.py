#!/usr/bin/env python3

from sys import argv
from os.path import isfile, isdir, exists

from typing import Final

from split import split_unquoted
from ui_element import UIElement

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_PAREN:   Final[str] = '{'
CLOSE_PAREN:  Final[str] = '}'

COMMA_DELIM:  Final[str] = ", "
OF_DELIM:     Final[str] = " of "

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

file_path: Final[str] = argv[1] if ARGC >= 2 else input("Enter input filepath >>> ")

# Check the path's validity
if not exists(file_path): raise FileNotFoundError(f"Could not find file '{file_path}'")
if 		isdir(file_path): raise IsADirectoryError(f"{file_path} is a directory")
if not isfile(file_path): raise        ValueError(f"{file_path} is not a text file")

# Read the file
with open(file_path, 'r') as f:
    file_contents: str = f.read().strip()

# Check that the stripped file is just one line long
if file_contents.count(NEWLINE) != 0: raise ValueError("File must be a single line")

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

# If the file starts or ends with curly braces, remove them
if file_contents[0]  == OPEN_PAREN:  file_contents = file_contents[1:]
if file_contents[-1] == CLOSE_PAREN: file_contents = file_contents[:-1]

# Split the file at every unquoted instance of ", "
file_lines: list[str] = split_unquoted(COMMA_DELIM, file_contents)

# Create a dictionary for each line,
#  and split each line at " of "
line_indents: list[dict[str, int | list[str]]] = []

for line in file_lines:
    segments: list[str] = split_unquoted(OF_DELIM, line)
    ui_elems: list[UIElement] = [UIElement(segment) for segment in segments]

    line_indents.append({
        "indent": 0,
        "content": ui_elems
    })

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

for line in line_indents:
    print(line["indent"], *map(str, line["content"]), sep='\t')
