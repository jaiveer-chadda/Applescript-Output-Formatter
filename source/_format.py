from typing import Callable, Final

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

type __fmt_func = Callable[[str], str]

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

__BLOCK_SIZE:   Final[int] = 3
__INT_SEP_CHAR: Final[str] = '_'

__RST:    Final[str] = "\033[0m"
__ITALIC: Final[str] = "\033[3m"
__BOLD:   Final[str] = "\033[1m"

__RED:    Final[str] = "\033[31m"
__GREEN:  Final[str] = "\033[32m"
__BLUE:   Final[str] = "\033[34m"
__PURPLE: Final[str] = "\033[35m"
__ORANGE: Final[str] = "\033[38;5;216m"

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

VALUE_: Final[str] = __ORANGE + __ITALIC + "value" + __RST
OP_BR_: Final[str] = __RED               + '('     + __RST
CL_BR_: Final[str] = __RED               + ')'     + __RST

error_: Final[__fmt_func] = lambda s: __RED    + __BOLD   +     s    + __RST
title_: Final[__fmt_func] = lambda s: __PURPLE + __ITALIC +     s    + __RST
float_: Final[__fmt_func] = lambda s: __PURPLE            +     s    + __RST
str_:   Final[__fmt_func] = lambda s: __GREEN             + f"'{s}'" + __RST

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def int_(input_: int) -> str:

    input_delimited = "".join([
        (__INT_SEP_CHAR if not i % __BLOCK_SIZE else '') + ii
        for i, ii in enumerate(str(input_)[::-1])
    ])[::-1].strip(__INT_SEP_CHAR)

    return __BLUE + input_delimited + __RST
