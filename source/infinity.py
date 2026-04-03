from sys import maxsize as MAXSIZE
from typing import Final, Self

from _format import *


class Infinity(float):

    __valid_input_types = str | int | float | None

    __VALID_FLOAT_STRS: Final[tuple[str, ...]] = ("inf", "infinity", "+inf", "+infinity")
    __VALID_INPUT_STRS: Final[tuple[str, ...]] = ("", '∞', "+∞", "None", *__VALID_FLOAT_STRS)

    __INFINITY_SIGN: Final[str] = '∞'

    __VALUE_ERROR_MSG: Final[str] = f"""
    {error_('Error: Invalid input')}; {VALUE_} must be one of:
      - {title_('None')} (a Nonetype value)

      - an {title_('int')} where {VALUE_} >= {int_(MAXSIZE)}

      - a {title_('float')} (case-insensitive):
          - {float_('float')}{OP_BR_}{str_('inf')}{CL_BR_}
          - {float_('float')}{OP_BR_}{str_('infinity')}{CL_BR_}
          - {float_('float')}{OP_BR_}{str_('+inf')}{CL_BR_}
          - {float_('float')}{OP_BR_}{str_('+infinity')}{CL_BR_}

      - a {title_('str')} (case-insensitive):
          - {str_('')}
          - {str_('∞')}
          - {str_('inf')}
          - {str_('infinity')}
          - {str_('+∞')}
          - {str_('+inf')}
          - {str_('+infinity')}
          - {str_('None')}
    """.replace(f"\n{' '*4}", "\n").strip()

    def __new__(cls: type[Self], value: __valid_input_types = None) -> Infinity:

        _value_str: Final[str] = str(value).lower()

        match value:
            case   None:                                          pass
            case   int() if value >= MAXSIZE:                     pass
            case   str() if _value_str in cls.__VALID_INPUT_STRS: pass
            case float() if _value_str in cls.__VALID_FLOAT_STRS: pass
            case _:
                raise ValueError(cls.__VALUE_ERROR_MSG)
        
        new_instance: Final[Infinity] = super().__new__(cls, "inf")

        return new_instance

    def __str__(self) -> str:
        return self.__INFINITY_SIGN
    
    def __repr__(self) -> str:
        return "Infinity()"
