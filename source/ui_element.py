from re import findall
from typing import Any, Callable, Final, Optional

from split import split_unquoted

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

match_tuple = tuple[str | None, str | None, str | None]

# —————————————————————————————————————————————————— #

OF_DELIM: Final[str] = " of "

_TYPE_REGEX: Final[str] = '([^"]+?)'
_IDX_REGEX:  Final[str] = '(\\d+)'
_NAME_REGEX: Final[str] = '"(.+?)"'

_MATCH_ALL_REGEX: Final[str] = f"{_TYPE_REGEX} (?:{_IDX_REGEX}|{_NAME_REGEX})$"

# —————————————————————————————————————————————————— #

is_string: Final[Callable[[Any], bool]] = lambda x: isinstance(x, str)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

class UIElement:

    def __init__(self: UIElement, input_: str | list[str]) -> None:

        _all_segments: list[str] = split_unquoted(OF_DELIM, input_) if is_string(input_) else input_
        self.parent: Optional[UIElement] = UIElement(_all_segments[1:]) if len(_all_segments) >= 2 else None

        _parse_result: Final[match_tuple] = self._parse_raw_elem_name(_all_segments[0])

        self.type:          str  =     _parse_result[0]
        self.idx:  Optional[int] = int(_parse_result[1]) if _parse_result[1] else None
        self.name: Optional[str] =     _parse_result[2]  if _parse_result[2] else None

        self.iden: str | int = self.name if self.name else self.idx

    # ——————————————————————————————————————————————————————————————————————————— #
    
    @property
    def id(self):
        return f"{id(self)}{(self._par_id_formatted())}"
    
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
    def _par_id_formatted(self) -> str: return f".{self.parent.id}"     if self.parent else ''

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
