from re import findall
from typing import Final, Optional


class UIElement:

    _TYPE_RE: Final[str] = '([^"]+?)'
    _IDX_RE:  Final[str] = '(\\d+)'
    _NAME_RE: Final[str] = '"(.+?)"'

    _MATCH_ALL_RE: Final[str] = f"{_TYPE_RE} (?:{_IDX_RE}|{_NAME_RE})$"


    def __init__(self: UIElement, string: str) -> None:
        matches: Final[list[str]] = findall(self._MATCH_ALL_RE, string)[0]

        self.type:          str  =     matches[0]
        self.idx:  Optional[int] = int(matches[1]) if matches[1] else None
        self.name: Optional[str] =     matches[2]  if matches[2] else None
        
        self.identifier:  str  = self.name if self.name else self.idx
        self._id_is_name: bool = bool(self.name)

    def _id_formatted(self) -> str:
        if self._id_is_name: return f'"{self.identifier}"'
        return self.identifier

    def _name_formatted(self) -> str:
        return f'"{self.name}"' if self.name else 'None'

    def __str__(self) -> str:
        return f"{self.type} {self._id_formatted()}"

    def __repr__(self) -> str:
        params: list[str] = [
            f"type: {self.type}",
            f"idx: {self.idx}",
            f"name: {self._name_formatted()}",
            f"identifier: {self._id_formatted()}"
        ]
        return f"UIElement({", ".join(params)})"
