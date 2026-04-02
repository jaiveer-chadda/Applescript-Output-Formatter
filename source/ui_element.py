from re import findall
from typing import Final, Optional


class UIElement:

    ##region 0 - Constants
    _TYPE_REGEX: Final[str] = '([^"]+?)'
    _IDX_REGEX:  Final[str] = '(\\d+)'
    _NAME_REGEX: Final[str] = '"(.+?)"'

    _MATCH_ALL_REGEX: Final[str] = f"{_TYPE_REGEX} (?:{_IDX_REGEX}|{_NAME_REGEX})$"
    ##endregion 0 - Constants


    ##region 1 - __init__
    def __init__(self: UIElement, string: str) -> None:
        _matches: Final[list[str]] = findall(self._MATCH_ALL_REGEX, string)[0]

        self.type:           str  =     _matches[0]
        self._idx:  Optional[int] = int(_matches[1]) if _matches[1] else None
        self._name: Optional[str] =     _matches[2]  if _matches[2] else None

        self._iden: str | int = self._name if self._name else self._idx
    ##endregion 1 - __init__


    ##region 2 - self.idx
    @property
    def idx(self) -> int | None: return self._idx
    
    @idx.setter
    def idx(self, val: int) -> None:
        self._idx  = val
        self._name = None
    ##endregion 2 - self.idx


    ##region 3 - self.name
    @property
    def name(self) -> str | None: return self._name

    @idx.setter
    def name(self, val: str) -> None:
        self._name = val
        self._idx  = None
    ##endregion 3 - self.name


    ##region 4 - self.iden
    @property
    def iden(self) -> str | int:
        return self.name if self.name else self.idx

    @iden.setter
    def iden(self, val: str | int) -> None:
        match val:
            case int(): self.idx  = val
            case str(): self.name = val
            case _: raise TypeError("Unsupported type")
    ##endregion 4 - self.iden


    ##region 5 - Dunder-Methods
    def __str__(self) -> str:
        return f"{self.type} {self._iden_formatted()}"

    def __repr__(self) -> str:
        return "".join((
            "UIElement(",
            f"type: {self.type}, ",

            f"name: {self._name_formatted()}" if self.name else
            f"idx: {self.idx}",
            ")"
        ))
    ##endregion 5 - Dunder-Methods


    ##region 6 - Helper-Functions
    def _iden_formatted(self) -> str: return f'"{self.iden}"' if self.name else self.iden
    def _name_formatted(self) -> str: return f'"{self.name}"' if self.name else None
    ##endregion 6 - Helper-Functions
