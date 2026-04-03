#!/usr/bin/env python3


from sys import argv
from os.path import isfile, isdir, exists

from typing import Final

from split import split_unquoted
from ui_element import UIElement


# ——— Constants ————————————————————————————————————————————————————————————————————————————————————————————————————— #

ln_obj = list[dict[str, int | UIElement]]

# —————————————————————————————————————————————————— #

ARGC: Final[int] = len(argv)

NEWLINE:      Final[str] = '\n'
OPEN_PAREN:   Final[str] = '{'
CLOSE_PAREN:  Final[str] = '}'

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
        _contents: str = f.read().strip()
    
    # ——————————————————————————————————————————————————————— #
    
    # Check that the stripped file is just one line long
    if _contents.count(NEWLINE) > 0:
        raise ValueError(NOT_SINGLE_LINE_ERR_MSG)

    return _contents


# ——— clean_file ———————————————————————————————————————————————————————————————————————————————————————————————————— #

def clean_file(_file_contents: str) -> str:
    _file_contents: str

    # If the file starts or ends with curly braces, remove them
    if _file_contents[0]  == OPEN_PAREN:  _file_contents = _file_contents[1:]
    if _file_contents[-1] == CLOSE_PAREN: _file_contents = _file_contents[:-1]
    
    return _file_contents


# ——— parse_file ———————————————————————————————————————————————————————————————————————————————————————————————————— #

def parse_file(_file_contents: str) -> ln_obj:
    # Split the file at every unquoted instance of ", "
    _file_lines: Final[list[str]] = split_unquoted(COMMA_DELIM, _file_contents)

    # Create a dictionary for each line
    return [
        {
            "indent": 0,
            "content": UIElement(_line)
        }
        for _line in _file_lines
    ]


# ——— main —————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def main() -> None:

    filepath: Final[str] = argv[1] if ARGC >= 2 else input(INPUT_PROMPT)

    raw_file_cont: Final[str]    =  read_file(filepath)
    file_contents: Final[str]    = clean_file(raw_file_cont)
    lines_object:  Final[ln_obj] = parse_file(file_contents)
    
    # ——————————————————————————————————————————————————————— #

    for line in lines_object:
        # print(line["indent"], line["content"])
        ui_elem: UIElement = line["content"]
        print(ui_elem.id(True))

    print(len(UIElement.all_UIElements))


if __name__ == "__main__":
    main()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
