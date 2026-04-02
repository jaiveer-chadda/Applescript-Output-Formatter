#!/usr/bin/env python3

from sys import argv
from os.path import isfile, isdir, exists
from re import Match, finditer, sub

from typing import Callable, Final, Iterator

from ui_element import UIElement  # ./ui_element.py

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_PAREN:   Final[str] = '{'
CLOSE_PAREN:  Final[str] = '}'
DOUBLE_QUOTE: Final[str] = '"'

COMMA_DELIM:  Final[str] = ", "
OF_DELIM:     Final[str] = " of "

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

_is_even:       Final[Callable[[int],      bool]] = lambda n        : n % 2 == 0
_is_unquoted:   Final[Callable[[int, str], bool]] = lambda idx, str_: _is_even(str_[:idx].count(DOUBLE_QUOTE))
_remove_prefix: Final[Callable[[str, str], str ]] = lambda pat, str_: sub(f"^{pat}", '', str_)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def split_unquoted(delim: str, str_to_split: str):

    # Get every instance of the delimiter in the string
    matches: Final[Iterator[Match[bytes]]] = finditer(delim, str_to_split)
    match_idxs: Final[list[int]] = [match.span()[0] for match in matches]

    # Iterate through the text, and split it at every instance of the delimiter
    #  which isn't inside quotes.
    # Also remove the delimiter from each line
    output_segments: list[str] = []

    for i, match_idx in enumerate(match_idxs):
        if _is_unquoted(match_idx, str_to_split):
            start_idx: int = match_idxs[i-1] if i != 0 else 0
            segment:   str = str_to_split[start_idx:match_idx]

            output_segments.append(_remove_prefix(delim, segment))

    return output_segments

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

# for line in line_indents: print(*line["content"], sep='\t')
for line in line_indents: print(line)
