#!/usr/bin/env python3

from sys import argv
from os.path import isfile, isdir, exists

from uuid import uuid8
from re import Match, finditer, sub

from typing import Callable, Final, Iterator

# ———————————————————————————————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_PAREN:   Final[str] = '{'
CLOSE_PAREN:  Final[str] = '}'
DOUBLE_QUOTE: Final[str] = '"'

DELIM: Final[str] = uuid8().hex
COMMA_DELIM: Final[str] = ", "

# ———————————————————————————————————————————————————————————————————————————— #

is_even: Final[Callable[[int], bool]] = lambda n: n % 2 == 0

def is_not_in_quotes(index: int, string: str) -> bool:
    left_quote_count: Final[int] = string[:index].count(DOUBLE_QUOTE)
    return is_even(left_quote_count)

def remove_prefix(pattern: str, string: str) -> str:
    return sub(f"^{pattern}", '', string)

# ———————————————————————————————————————————————————————————————————————————— #

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

# ———————————————————————————————————————————————————————————————————————————— #

# If the file starts or ends with curly braces, remove them
if file_contents[0]  == OPEN_PAREN:  file_contents = file_contents[1:]
if file_contents[-1] == CLOSE_PAREN: file_contents = file_contents[:-1]

# Get every instance of ", " in the file
all_commas: Final[Iterator[Match[bytes]]] = finditer(COMMA_DELIM, file_contents)
all_comma_idxs: Final[list[int]] = [match.span()[0] for match in all_commas]


# Iterate through the text, and split it at every instance of ", "
#   which isn't inside quotes.
# Also remove the comma sequences from each line
file_lines: list[str] = []

for i, comma_idx in enumerate(all_comma_idxs):
    if is_not_in_quotes(comma_idx, file_contents):
        start_idx: int = all_comma_idxs[i-1] if i != 0 else 0
        segment:   str = file_contents[start_idx:comma_idx]

        file_lines.append(remove_prefix(COMMA_DELIM, segment))

# Create a dictionary for each line
lines_dicts: list[dict[str, str | int]] = [
    { "indent": 0,
      "content": line
    } for line in file_lines
]
