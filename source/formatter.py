#!/usr/bin/env python3

from sys import argv
from os.path import isfile, isdir, exists

from typing import Final

from split import split_unquoted
from ui_element import UIElement

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

ln_obj = list[dict[str, int | list[UIElement]]]

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_PAREN:   Final[str] = '{'
CLOSE_PAREN:  Final[str] = '}'

COMMA_DELIM:  Final[str] = ", "
OF_DELIM:     Final[str] = " of "

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def read_file(_filepath: str) -> str:

    # Check the path's validity
    if not exists(_filepath): raise FileNotFoundError(f"Could not find file '{_filepath}'")
    if 		isdir(_filepath): raise IsADirectoryError(f"{_filepath} is a directory")
    if not isfile(_filepath): raise        ValueError(f"{_filepath} is not a text file")

    # Read the file
    with open(_filepath, 'r') as f:
        _file_contents: str = f.read().strip()

    # Check that the stripped file is just one line long
    if _file_contents.count(NEWLINE) > 0: raise ValueError("File must be a single line")

    return _file_contents

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def clean_file(_file_contents: str) -> str:

    # If the file starts or ends with curly braces, remove them
    if _file_contents[0]  == OPEN_PAREN:  new_file_contents = _file_contents[1:]
    if _file_contents[-1] == CLOSE_PAREN: new_file_contents = _file_contents[:-1]
    
    return new_file_contents

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #


def parse_file(_file_contents: str) -> ln_obj:
    # Split the file at every unquoted instance of ", "
    _file_lines: Final[list[str]] = split_unquoted(COMMA_DELIM, _file_contents)

    # Create a dictionary for each line,
    #  and split each line at " of "
    _lines_obj: ln_obj = []

    for _line in _file_lines:
        _segments: list[str] = split_unquoted(OF_DELIM, _line)
        _ui_elems: list[UIElement] = [UIElement(segment) for segment in _segments]

        _lines_obj.append({
            "indent": 0,
            "content": _ui_elems
        })
        
    return _lines_obj

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #


def main() -> None:
    filepath: Final[str] = argv[1] if ARGC >= 2 else input("Enter input filepath >>> ")

    raw_file_cont: Final[str]    =  read_file(filepath)
    file_contents: Final[str]    = clean_file(raw_file_cont)
    lines_object:  Final[ln_obj] = parse_file(file_contents)

    for line in lines_object:
        print(line["indent"], *map(str, line["content"]), sep='\t')


if __name__ == "__main__":
    main()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
