#!/usr/bin/env python3


from sys import argv
from os.path import isfile, isdir, exists

from typing import Final

from split import split_unquoted
from ui_element import UIElement
from infinity import Infinity


# ——— Constants ————————————————————————————————————————————————————————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_BRACE:   Final[str] = '{'
CLOSE_BRACE:  Final[str] = '}'

COMMA_DELIM:  Final[str] = ", "
INPUT_PROMPT: Final[str] = "Enter input filepath >>> "


# ——— read_file ————————————————————————————————————————————————————————————————————————————————————————————————————— #

def read_file(file: str) -> str:

    FILE_NOT_FOUND_ERR_MSG:  Final[str] = f"Could not find file '{file}'."
    IS_A_DIRECTORY_ERR_MSG:  Final[str] = f"{file} is a directory."
    NOT_TEXT_FILE_ERR_MSG:   Final[str] = f"{file} is not a text file."
    NOT_SINGLE_LINE_ERR_MSG: Final[str] = "File must be a single line."

    # ——————————————————————————————————————————————————————— #

    # Check the path's validity
    if not exists(file): raise FileNotFoundError(FILE_NOT_FOUND_ERR_MSG)
    if 		isdir(file): raise IsADirectoryError(IS_A_DIRECTORY_ERR_MSG)
    if not isfile(file): raise        ValueError(NOT_TEXT_FILE_ERR_MSG)

    # Read the file
    with open(file, 'r') as f:
        contents: Final[str] = f.read().strip()

    # ——————————————————————————————————————————————————————— #

    # Check that the stripped file is just one line long
    if contents.count(NEWLINE) > 0:
        raise ValueError(NOT_SINGLE_LINE_ERR_MSG)

    return contents


# ——— clean_file ———————————————————————————————————————————————————————————————————————————————————————————————————— #

def clean_file(contents: str) -> str:

    # If the file starts or ends with curly braces, remove them
    if contents[0]  == OPEN_BRACE:  contents = contents[1:]
    if contents[-1] == CLOSE_BRACE: contents = contents[:-1]

    return contents


# ——— parse_file ———————————————————————————————————————————————————————————————————————————————————————————————————— #

def parse_file(contents: str) -> list[UIElement]:
    # Split the file at every unquoted instance of ", "
    _file_lines: Final[list[str]] = split_unquoted(COMMA_DELIM, contents)

    # Create a UIElement object out of each line
    return [UIElement(_file_lines[0])]
    # return [UIElement(line) for line in _file_lines]


# ——— main —————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def main() -> None:

    filepath: Final[str] = argv[1] if ARGC >= 2 else input(INPUT_PROMPT)

    raw_file_cont: Final[str]             =  read_file(filepath)
    file_contents: Final[str]             = clean_file(raw_file_cont)
    ui_elems_obj:  Final[list[UIElement]] = parse_file(file_contents)

    # ——————————————————————————————————————————————————————— #
    
    for ui_elem in ui_elems_obj[:32]: print(                     ui_elem.id_at_level(Infinity(), colour='indent'))
    for ui_elem in ui_elems_obj[:32]: print('\t'*ui_elem.indent, ui_elem.   at_level(Infinity(), colour='indent'))


if __name__ == "__main__":
    main()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
