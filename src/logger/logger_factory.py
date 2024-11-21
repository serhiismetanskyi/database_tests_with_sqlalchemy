import logging
from logging import Formatter, LogRecord
from typing import Any


class LoggerFormatter(Formatter):
    def __init__(self, default_formatter: Formatter) -> None:
        super().__init__()
        self.default_formatter = default_formatter

    def format(self, record: LogRecord) -> str:
        record.msg = f"[{record.name}] [{record.levelname}] {record.msg}"
        return self.default_formatter.format(record)


def factory(fmt: str, datefmt: str, *args: Any) -> Formatter:
    formatter: Formatter = logging.Formatter(fmt, datefmt, *args)
    return LoggerFormatter(default_formatter=formatter)
