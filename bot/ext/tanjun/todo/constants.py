import string

from bot.ext.tanjun.todo.struct import TokenType

IDENTIFIER_CHARS = tuple(string.ascii_letters)
KEYWORDS = {"when": TokenType.WHEN, "do": TokenType.DO, "at": TokenType.AT}
