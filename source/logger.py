#!/usr/bin/env python3


from loguru import logger

import re
from sys import stderr
from inspect import FrameInfo, stack

from typing import Callable, Final


class Log:

    fmt = str

    _MSG_SEP:  Final[str] = '│'
    _LINE_CHR: Final[str] = '─'

    _level_col: Final[Callable[[str], str]] = lambda s: f"<level>{s}</level>"

    def __init__(self) -> None:
        self.log_format:   Log.fmt
        self.start_format: Log.fmt

        self._init_formats()
        self._set_default_logger()

        try: logger.level("START", no=0, color="<green>")
        except ValueError: pass


    def _init_formats(self) -> None:
        _time:     Log.fmt = "\x1b[2m{time:HH:mm:}\x1b[0m{time:ss.SSSS}"
        _level:    Log.fmt = Log._level_col("[{level}]") + ' '*2
        _location: Log.fmt = "{module} : {function} : {line}"
        _sep:      Log.fmt = "\x1b[32m" + self._MSG_SEP + "\x1b[0m"
        _message:  Log.fmt = "\b" + Log._level_col("{message}")

        all_fmts: tuple[Log.fmt, ...] = (_time, _level, _location, _sep, _message)

        self.log_format = '\t'.join(all_fmts)
        self.start_format = f"{_time}  <level>{self._LINE_CHR*4} {{message}}┼{self._LINE_CHR*120}</level>"


    def _set_default_logger(self) -> None:
        logger.remove()
        logger.add(sink=stderr, level=5, format=self.log_format, colorize=True)

    def _set_start_logger(self) -> None:
        logger.remove()
        logger.add(sink=stderr, level=0, format=self.start_format, colorize=True)


    trace   = logger.trace
    debug   = logger.debug
    info    = logger.info
    success = logger.success
    warning = logger.warning
    error   = logger.error


    def start(self) -> None:
        self._set_start_logger()
        _caller_info:   Final[list[FrameInfo]] = stack()[1]

        _caller_name:   Final[FrameInfo] = _caller_info[3]
        _caller_module: Final[FrameInfo] = _caller_info[1]

        _module_name: Final[str] = re.sub("(?:^.*/)|\\.py$", '', _caller_module)
        _message:     Final[str] = f"{_module_name} : {_caller_name} ".ljust(28, '─')

        logger.log("START", _message)
        self._set_default_logger()


log = Log()


def main() -> None:

    log.start      ()
    logger.trace   ( "c'est un trace"    " msg" )
    log.trace      ( "c'est un trace"    " msg" )
    logger.debug   ( "c'est un debug"    " msg" )
    log.debug      ( "c'est un debug"    " msg" )
    logger.info    ( "c'est un info"     " msg" )
    log.info       ( "c'est un info"     " msg" )
    logger.success ( "c'est un success"  " msg" )
    log.success    ( "c'est un success"  " msg" )
    logger.warning ( "c'est un warning"  " msg" )
    log.warning    ( "c'est un warning"  " msg" )
    logger.error   ( "c'est un error"    " msg" )
    log.error      ( "c'est un error"    " msg" )


if __name__ == "__main__":
    main()
    log.start()
