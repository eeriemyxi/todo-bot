from dataclasses import dataclass
from enum import Enum, auto

__all__ = ("Day", "Time", "WhenKeyword", "AtKeyword", "DoKeyword", "TokenType", "Token")


class Day(Enum):
    TODAY = 1
    TOMORROW = 2


@dataclass
class Time:
    hour: int
    minute: int


@dataclass
class WhenKeyword:
    literal: str
    day: Day


@dataclass
class AtKeyword:
    literal: str
    time: Time


@dataclass
class DoKeyword:
    literal: str
    description: str


class TokenType(Enum):
    WHEN = auto()
    AT = auto()
    DO = auto()


@dataclass
class Token:
    token_type: TokenType
    data: WhenKeyword | AtKeyword | DoKeyword
