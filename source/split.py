from re import Match, finditer, sub

from typing import Callable, Final, Iterator

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

DOUBLE_QUOTE: Final[str] = '"'

_is_even:       Final[Callable[[int],           bool]] = lambda num:           num % 2 == 0
_is_unquoted:   Final[Callable[[int, str, str], bool]] = lambda idx, str, qot: _is_even(str[:idx].count(qot))
_remove_prefix: Final[Callable[[str, str],      str ]] = lambda pat, str:      sub(f"^{pat}", "", str)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def split_unquoted(delim: str, str_to_split: str, quote_type: str = DOUBLE_QUOTE) -> list[str]:

    # Get every instance of the delimiter in the string
    _matches: Final[Iterator[Match[str]]] = finditer(delim, str_to_split)
    _match_idxs: Final[list[int]] = [match.span()[0] for match in _matches]

    # If there aren't any matches, then there's just one segment
    if len(_match_idxs) == 0:
        return [str_to_split]

    # Iterate through the text, and split it at every instance of the delimiter
    #  which isn't inside quotes.
    # Also remove the delimiter from each line
    output_segments: list[str] = []

    for i, match_idx in enumerate(_match_idxs):
        if _is_unquoted(match_idx, str_to_split, quote_type):
            _start_idx: int = _match_idxs[i-1] if i != 0 else 0
            _segment:   str = str_to_split[_start_idx:match_idx]

            output_segments.append(_remove_prefix(delim, _segment))

    _trailing_segment: Final[str] = str_to_split[match_idx:]
    output_segments.append(_remove_prefix(delim, _trailing_segment))

    return output_segments
