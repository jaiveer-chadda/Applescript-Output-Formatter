from re import findall
from uuid import uuid8
from random import randrange, seed as set_seed

from typing import Any, Callable, Final, Optional

from split import split_unquoted

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

match_tuple = tuple[str, Optional[int], Optional[str]]

# —————————————————————————————————————————————————— #

OF_DELIM:    Final[str] = " of "
_LIST_DELIM: Final[str] = str(uuid8())  # '▄'  # (for debugging)

_TYPE_REGEX: Final[str] = '([^"]+?)'
_IDX_REGEX:  Final[str] = '(\\d+)'
_NAME_REGEX: Final[str] = '"(.+?)"'

_MATCH_ALL_REGEX: Final[str] = f"{_TYPE_REGEX} (?:{_IDX_REGEX}|{_NAME_REGEX})$"

# —————————————————————————————————————————————————— #

_is_string: Final[Callable[[Any],       bool]] = lambda x: isinstance(x, str)
_join_list: Final[Callable[[list[str]], str ]] = lambda x: _LIST_DELIM.join(x)
_rand_col:  Final[Callable[[],          str ]] = lambda:   str(randrange(100, 255))

def _random_colour(seed: Any) -> str:
    set_seed(seed)
    rgb: tuple[str, ...] = (_rand_col(), _rand_col(), _rand_col())
    return f"\033[38;2;{';'.join(rgb)}m"


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

class UIElement:

    all_UIElements: dict[str, UIElement] = {}
    __all_segments: list[str]

    # ——————————————————————————————————————————————————————————————————————————— #

    def __new__(cls: UIElement, input_: str | list[str]) -> UIElement:
        # I know this probably isn't best practice, but I'm computing this here,
        #  then passing it to __init__ later on - so I don't need to duplicate any code
        cls.__all_segments = split_unquoted(OF_DELIM, input_) if _is_string(input_) else input_

        # Initialise a new UIElement
        new_instance: UIElement = super().__new__(cls)

        # Work out the unique id and assign it to the new instance
        _unique_id: int = _join_list(cls.__all_segments)
        new_instance.unique_id = _unique_id

        # If an object with the same inputs already exists,
        #  then just return the existing one
        if new_instance.unique_id in cls.all_UIElements:
            return cls.all_UIElements[_unique_id]

        # Otherwise, cache the new object, and return it
        cls.all_UIElements[_unique_id] = new_instance
        return new_instance

    # ——————————————————————————————————————————————————————————————————————————— #

    def __init__(self: UIElement, _) -> None:

        # Read in the segments which were pre-computed in __new__
        _all_segments: list[str] = self.__all_segments

        # Use regex to find type and identifier of the first segment
        #  Then unpack the parsed results, and convert them to their proper types if needed
        self.type, self.idx, self.name = self._parse_raw_elem_name(_all_segments[0])

        # Determine which of self.idx or self.name is valid - this'll be the element's identifier
        self.iden: str | int = self.name if self.name is not None else self.idx

        # Just a note to self that self._unique_id does exist, but is assigned in __new__
        self.unique_id: int

        # Recursively parse the element's parents by handing the constructor all remaining segments
        #  But only do so if there are actually any segments left
        _remaining_segs: list[str] = _all_segments[1:]
        self.parent: Optional[UIElement] = UIElement(_remaining_segs) if len(_remaining_segs) != 0 else None

    # ——————————————————————————————————————————————————————————————————————————— #

    def id(self, do_colour: bool = False) -> str:
        _colour: Final[str] = "" if not do_colour else _random_colour(seed=self.unique_id)
        _reset:  Final[str] = "" if not do_colour else "\033[0m"

        _parent: Final[str] = f".{self.parent.id(do_colour)}" if self.parent else ''
        return f"{_colour}{id(self)}{_reset}{_parent}"

    # ——————————————————————————————————————————————————————————————————————————— #

    def _parse_raw_elem_name(self, raw_name: str) -> match_tuple:
        _parse_result: Final[list[str]] = findall(_MATCH_ALL_REGEX, raw_name)[0]

        type_: Final[str]           =     _parse_result[0]
        idx:   Final[Optional[int]] = int(_parse_result[1]) if _parse_result[1] != '' else None
        name:  Final[Optional[str]] =     _parse_result[2]  if _parse_result[2] != '' else None
        return (type_, idx, name)

    # ——————————————————————————————————————————————————————————————————————————— #

    def __str__(self) -> str:
        return f"{self.type} {self._iden_formatted()}{self._parent_formatted()}"
        # # For Debugging
        # type_: str = self.type.replace("application", "app")
        # iden_: str = str(self._iden_formatted()).replace(" All Raycast Extensions.scpt", "...scpt")
        # return f"{type_} {iden_}{self._parent_formatted()}"

    def __repr__(self) -> str:
        return f"UIElement(type: {self.type}, iden: {self._iden_formatted()}, parent: {str(self.parent)})"

    # ——————————————————————————————————————————————————————————————————————————— #

    def   _iden_formatted(self) -> str: return f'"{self.name}"'         if self.name   else str(self.idx)
    def   _name_formatted(self) -> str: return f'"{self.name}"'         if self.name   else None
    def _parent_formatted(self) -> str: return f" / {str(self.parent)}" if self.parent else ''

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
