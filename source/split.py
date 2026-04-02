from re import Match, finditer, sub

from typing import Callable, Final, Iterator

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

DOUBLE_QUOTE: Final[str] = '"'

_is_even:       Final[Callable[[int],      bool]] = lambda n        : n % 2 == 0
_is_unquoted:   Final[Callable[[int, str], bool]] = lambda idx, str_: _is_even(str_[:idx].count(DOUBLE_QUOTE))
_remove_prefix: Final[Callable[[str, str], str ]] = lambda pat, str_: sub(f"^{pat}", '', str_)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

def split_unquoted(delim: str, str_to_split: str):

    # Get every instance of the delimiter in the string
    matches: Final[Iterator[Match[bytes]]] = finditer(delim, str_to_split)
    match_idxs: Final[list[int]] = [match.span()[0] for match in matches]

    # Iterate through the text, and split it at every instance of the delimiter
    #  which isn't inside quotes.
    # Also remove the delimiter from each line
    output_segments: list[str] = []

    for i, match_idx in enumerate(match_idxs):
        if _is_unquoted(match_idx, str_to_split):
            start_idx: int = match_idxs[i-1] if i != 0 else 0
            segment:   str = str_to_split[start_idx:match_idx]

            output_segments.append(_remove_prefix(delim, segment))

    return output_segments

