from re import findall
from typing import Final, Optional

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

class UIElement:

    _TYPE_REGEX: Final[str] = '([^"]+?)'
    _IDX_REGEX:  Final[str] = '(\\d+)'
    _NAME_REGEX: Final[str] = '"(.+?)"'

    _MATCH_ALL_REGEX: Final[str] = f"{_TYPE_REGEX} (?:{_IDX_REGEX}|{_NAME_REGEX})$"

# ——————————————————————————————————————————————————————————————————————————— #

    def __init__(self: UIElement, string: str) -> None:
        _matches: Final[list[str]] = findall(self._MATCH_ALL_REGEX, string)[0]

        self.type:          str  =     _matches[0]
        self.idx:  Optional[int] = int(_matches[1]) if _matches[1] else None
        self.name: Optional[str] =     _matches[2]  if _matches[2] else None

        self.iden: str | int = self.name if self.name else self.idx

# ——————————————————————————————————————————————————————————————————————————— #

    def _iden_formatted(self) -> str: return f'"{self.iden}"' if self.name else self.iden
    def _name_formatted(self) -> str: return f'"{self.name}"' if self.name else None

# ——————————————————————————————————————————————————————————————————————————— #

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

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
