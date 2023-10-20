from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

__all__ = ("Day", "Time", "TokenType", "Token")


class Day(Enum):
    TODAY = 1
    TOMORROW = 2


@dataclass
class Time:
    hour: int
    minute: int


class TokenType(Enum):
    WHEN = auto()
    AT = auto()
    DO = auto()

    STRING = auto()
    TIME = auto()

    EOF = auto()


@dataclass
class Token:
    token_type: TokenType
    literal: str
    cols: tuple[int, int]
    data: Any | None = None
