from enum import IntEnum, auto


class TokenType(IntEnum):
    INT = auto()
    FLOAT = auto()
    SYMBOL = auto()
    STRING = auto()
    LPAREN = auto()
    RPAREN = auto()
    IF = auto()
    BINARY_OP = auto()
    KEYWORD = auto()


class Token:
    def __init__(self, token_type: TokenType, literal: str) -> None:
        self.token_type = token_type
        self.literal = literal

    def __eq__(self, __o: object) -> bool:
        if __o is None or not isinstance(__o, Token):
            return False
        return self.token_type == __o.token_type and self.literal == __o.literal

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return self.literal
