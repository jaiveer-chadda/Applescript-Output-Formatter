from re import findall
from uuid import uuid8
from random import randrange, seed as set_seed

from typing import Annotated, Any, Callable, Final, Optional, Self

from split import split_unquoted
from infinity import Infinity

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

INFINITY: Final[Infinity] = Infinity()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

class UIElement:
    
    # —— Constants / Declarations —————————————————————————————————————————————————————— #
    # ———— Types ————————————————————————————————————————— #
    
    match_tuple = tuple[str, Optional[int], Optional[str]]
    
    # ———— Constants ————————————————————————————————————— #

    __PARENT_SEPARATOR: Final[str] = " / "
    __ID_SEPARATOR:     Final[str] = '.'
    __ATTR_SEPARATOR:   Final[str] = ", "

    __OF_DELIM:   Final[str] = " of "
    __LIST_DELIM: Final[str] = str(uuid8())  # '▄'  # (for debugging)

    __TYPE_REGEX: Final[str] = '([^"]+?)'
    __IDX_REGEX:  Final[str] = '(\\d+)'
    __NAME_REGEX: Final[str] = '"(.+?)"'

    __MATCH_ALL_REGEX: Final[str] = f"{__TYPE_REGEX} (?:{__IDX_REGEX}|{__NAME_REGEX})$"
    
    # ———— Class Objects ————————————————————————————————— #

    __all_UIElements: dict[str, UIElement] = {}
    __all_segments: list[str]

    __do_colour: bool = False
    __reset_col: str = ""

    # —— __new__() ————————————————————————————————————————————————————————————————————— #

    def __new__(cls: type[Self], input_: str | list[str]) -> UIElement:

        # I know this probably isn't best practice, but I'm computing this here,
        #  then passing it to __init__ later on - so I don't need to duplicate any code
        cls.__all_segments = (
            split_unquoted(cls.__OF_DELIM, input_)  # type: ignore
            if cls.__is_string(input_) else
            input_
        )

        # Initialise a new UIElement
        new_instance: UIElement = super().__new__(cls)

        # Work out the unique id and assign it to the new instance
        __unique_id: str = cls.__join_list(cls.__all_segments)
        new_instance._unique_id = __unique_id

        # If an object with the same inputs already exists,
        #  then just return the existing one
        if new_instance._unique_id in cls.__all_UIElements:
            return cls.__all_UIElements[__unique_id]

        # Otherwise, cache the new object, and return it
        cls.__all_UIElements[__unique_id] = new_instance
        return new_instance


    # —— __init__() ———————————————————————————————————————————————————————————————————— #

    def __init__(self: UIElement, _) -> None:

        # Read in the segments which were pre-computed in __new__
        _all_segments: list[str] = self.__all_segments

        # Use regex to find type and identifier of the first segment
        #  Then unpack the parsed results, and convert them to their proper types if needed
        self.__init_identifiers(_all_segments[0])

        # Determine which of self.idx or self.name is valid - this'll be the element's identifier
        self.iden: str | int = self.name if self.name is not None else self.idx  # type: ignore

        # Just a note to self that self.__unique_id does exist, but is assigned in __new__
        self._unique_id: str

        # Also initialise a few other attributes that I'll use later
        self.__colour: str = ""
        self.parent: Optional[UIElement]
        self.depth: int
        
        # Initialise each object's unique colour
        if self.__do_colour:
            self.__init_colour()

        # Recursively parse the element's parents by handing the constructor all remaining segments
        #  But only do so if there are actually any segments left
        _remaining_segs: list[str] = _all_segments[1:]

        if len(_remaining_segs) == 0:
            self.parent = None
            self.depth = 0
            return

        self.parent = UIElement(_remaining_segs)
        self.depth = self.parent.depth + 1


    # —— __Initialisation Functions ———————————————————————————————————————————————————— #

    def __init_identifiers(self, raw_name: str) -> None:
        _parse_result: Final[list[str]] = findall(self.__MATCH_ALL_REGEX, raw_name)[0]

        self.type: str           =     _parse_result[0]
        self.idx:  Optional[int] = int(_parse_result[1]) if _parse_result[1] != '' else None
        self.name: Optional[str] =     _parse_result[2]  if _parse_result[2] != '' else None


    def __init_colour(self, _seed: Annotated[Optional[Any], "default: self._unique_id"] = None) -> None:
        set_seed(self._unique_id if _seed is None else _seed)
        self.__colour = f"\033[38;2;{';'.join(self.__rand_rgb())}m"


    # —— Class Methods ————————————————————————————————————————————————————————————————— #

    @classmethod
    def get_all(cls, _get_dict: bool = False) -> tuple[UIElement, ...] | dict[str, UIElement]:
        if _get_dict:
            return cls.__all_UIElements
        return tuple(cls.__all_UIElements.values())

    @classmethod
    def do_colour(cls, set: bool = True) -> None:
        cls.__reset_col: str = "\033[0m" if set else ""
        cls.__do_colour = set


    # —— Computed Properties ——————————————————————————————————————————————————————————— #
    
    @property
    def base(self) -> str:
        return self.at_level(0)
    
    @property
    def id(self) -> str:
        return self.id_at_level(INFINITY)


    # —— Public Methods ———————————————————————————————————————————————————————————————— #
    
    def at_level(self, level: int, *, sep: str = __PARENT_SEPARATOR) -> str:
        return self._get_str(level, sep)
    
    def id_at_level(self, level: int | Infinity, sep: str = __ID_SEPARATOR) -> str:
        return self._get_id(level, sep)


    # —— _Private Methods —————————————————————————————————————————————————————————————— #

    def _get_str(self, _level: int, _sep: str) -> str:
        parent: str = (
            f"{_sep}{self.parent._get_str(_level-1, _sep)}"
            if self.parent is not None and _level > 0
            else ""
        )
        return f"{self.type} {self.__iden_fmtd()}{parent}"


    def _get_id(self, _level: int | Infinity, _sep: str) -> str:
        _parent: Final[str] = (
            f"{_sep}{self.parent._get_id(_level-1, _sep)}" if self.parent and _level > 0  # type: ignore
            else ''
        )
        return f"{self.__colour}{id(self)}{self.__reset_col}{_parent}"
    

    # —— __Dunder Methods__ ———————————————————————————————————————————————————————————— #

    def  __str__(self) -> str:
        return self.at_level(0)  #FIX


    def __repr__(self) -> str:
        _attrs: tuple[str, ...] = (
            f"type: {self.type}",
            ( # print the correct identifier, based on which one's active
                f"name: {self.name}" if self.name else
                f"idx: {self.idx}"
            ),
            f"parent: {str(self.parent)}",
            f"depth: {self.depth}"
        )

        return (f"UIElement({self.__ATTR_SEPARATOR.join(_attrs)})")


    # —— __Helper Functions ———————————————————————————————————————————————————————————— #

    __iden_fmtd: Final[Callable[[Self],      str ]] = lambda s: f'"{s.name}"' if s.name else str(s.idx)
    __is_string: Final[Callable[[Any],       bool]] = lambda x: isinstance(x, str)
    __join_list: Final[Callable[[list[str]], str ]] = lambda x: UIElement.__LIST_DELIM.join(x)

    __rand_col:  Final[Callable[[],          str ]] = lambda:   str(randrange(100, 255))
    __rand_rgb:  Final[Callable[[Self], list[str]]] = lambda _: [UIElement.__rand_col() for _ in range(3)]


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #
