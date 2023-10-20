from bot.ext.tanjun.todo import constants
from bot.ext.tanjun.todo.struct import Time, Token, TokenType


class TokenScanner:
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: list = []
        self.token_start_pos: int = 0
        self.cur_pos: int = 0
        self.token_start_col: int = self.cur_pos
        self.token_end_col: int = self.cur_pos

    def is_at_end(self) -> bool:
        return self.cur_pos >= len(self.source)

    def advance(self, *, no_col: bool = False) -> str:
        cur_char = self.source[self.cur_pos]
        self.cur_pos += 1

        if not no_col:
            self.token_end_col += 1

        return cur_char

    def peek(self) -> str:
        return "" if self.is_at_end() else self.source[self.cur_pos]

    @property
    def cols(self) -> tuple[int, int]:
        return (self.token_start_col, self.token_end_col)

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.token_start_pos = self.cur_pos
            self.token_start_col = self.cur_pos
            self.token_end_col = self.cur_pos
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.cur_pos))

        return self.tokens

    def scan_token(self) -> None:
        char = self.advance(no_col=True)

        match char:
            case '"':
                self.handle_string()
            case " " | "\t":
                pass
            case _:
                if char.isdigit():
                    self.handle_number()
                elif char in constants.IDENTIFIER_CHARS:
                    self.handle_identifier()

    def handle_identifier(self) -> None:
        while self.peek() in constants.IDENTIFIER_CHARS:
            self.advance()

        identifier = self.source[self.token_start_pos : self.cur_pos]
        _type = constants.KEYWORDS.get(identifier)
        if _type:
            self.tokens.append(Token(_type, identifier, self.cols))
        else:
            self.tokens.append(Token(TokenType.STRING, identifier, self.cols))

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            self.advance()

        if self.is_at_end():
            # TODO: raise better exception
            raise Exception

        self.advance()

        string_value = self.source[self.token_start_pos + 1 : self.cur_pos - 1]
        self.tokens.append(Token(TokenType.STRING, string_value, self.cols))

    def handle_number(self) -> None:
        while self.peek().isdigit() or self.peek().isspace():
            self.advance()

        if self.peek() == ":":
            first_set_end = self.cur_pos

            self.advance()

            while self.peek().isdigit():
                self.advance()

            first_set = self.source[self.token_start_pos : first_set_end]
            second_set = self.source[first_set_end + 1 : self.cur_pos]

            self.tokens.append(
                Token(
                    TokenType.TIME,
                    self.source[self.token_start_pos : self.cur_pos],
                    self.cols,
                    Time(int(first_set), int(second_set)),
                )
            )
        else:
            # TODO: better exception
            raise Exception
