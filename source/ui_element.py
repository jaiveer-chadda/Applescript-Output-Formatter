from re import findall
from uuid import uuid8
from random import randrange, seed

from typing import Any, Callable, Final, Optional

from split import split_unquoted

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

match_tuple = tuple[str | None, str | None, str | None]

# —————————————————————————————————————————————————— #

OF_DELIM:    Final[str] = " of "
_HASH_DELIM: Final[str] = str(uuid8())

_TYPE_REGEX: Final[str] = '([^"]+?)'
_IDX_REGEX:  Final[str] = '(\\d+)'
_NAME_REGEX: Final[str] = '"(.+?)"'

_MATCH_ALL_REGEX: Final[str] = f"{_TYPE_REGEX} (?:{_IDX_REGEX}|{_NAME_REGEX})$"

# —————————————————————————————————————————————————— #

_is_string: Final[Callable[[Any],       bool]] = lambda x: isinstance(x, str)
_hash_list: Final[Callable[[list[str]], int ]] = lambda x: hash(_HASH_DELIM.join(x))

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

class UIElement:
    
    all_UIElements: set = set()

    def __init__(self: UIElement, input_: str | list[str]) -> None:
        
        self.hash: int = _hash_list(input_)
        self.all_UIElements.add(self.hash)

        _all_segments: list[str] = split_unquoted(OF_DELIM, input_) if _is_string(input_) else input_
        _parse_result: Final[match_tuple] = self._parse_raw_elem_name(_all_segments[0])

        self.type:          str  =     _parse_result[0]
        self.idx:  Optional[int] = int(_parse_result[1]) if _parse_result[1] else None
        self.name: Optional[str] =     _parse_result[2]  if _parse_result[2] else None

        self.iden: str | int = self.name if self.name else self.idx

        self.parent: Optional[UIElement] = UIElement(_all_segments[1:]) if len(_all_segments) >= 2 else None
        
    # ——————————————————————————————————————————————————————————————————————————— #
    
    def id(self, do_colour: bool = False):
        
        colour: str = ""
        reset:  str = ""

        if do_colour:
            reset = "\033[0m"

            seed(self.hash)
            r: int = randrange(50, 255)
            g: int = randrange(50, 255)
            b: int = randrange(50, 255)

            colour = f"\033[38;2;{r};{g};{b}m"

        parent = f".{self.parent.id(do_colour)}" if self.parent else ''
        
        return f"{colour}{id(self)}{parent}{reset}"
    
    # ——————————————————————————————————————————————————————————————————————————— #

    def _parse_raw_elem_name(self, raw_name: str) -> match_tuple:
        _parse_result: Final[list[str]] = findall(_MATCH_ALL_REGEX, raw_name)[0]

        return tuple([
            _match if _match != '' else None
            for _match in _parse_result
        ])

    # ——————————————————————————————————————————————————————————————————————————— #

    def __str__(self) -> str:
        # return f"{self.type} {self.iden}{self._parent_formatted()}"

        # this below is all temporary
        type_: str = self.type.replace("application", "app")
        iden_: str = str(self._iden_formatted()).replace(" All Raycast Extensions.scpt", "...scpt")
        return f"{type_} {iden_}{self._parent_formatted()}"

    def __repr__(self) -> str:
        return "".join((
            "UIElement(",
            f"type: {self.type}, ",

            f"name: {self._name_formatted()}" if self.name else
            f"idx: {self.idx}",
            f"parent: {str(self.parent)}",
            ")"
        ))

    # ——————————————————————————————————————————————————————————————————————————— #

    def   _iden_formatted(self) -> str: return f'"{self.iden}"'         if self.name   else self.iden
    def   _name_formatted(self) -> str: return f'"{self.name}"'         if self.name   else None
    def _parent_formatted(self) -> str: return f"\t/ {str(self.parent)}" if self.parent else ''

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
