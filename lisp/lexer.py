from abc import ABC
from enum import IntEnum, auto
from typing import List


class TokenType(IntEnum):
    INTEGER = auto()
    SYMBOL = auto()
    LPAREN = auto()
    RPAREN = auto()


class Token(ABC):
    token_type: TokenType

    def __eq__(self, other: object) -> bool:
        if other is None or type(self) != type(other):
            return False

        return self.token_type == other.token_type

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class Integer(Token):
    def __init__(self, i: int):
        self.token_type = TokenType.INTEGER
        self.i = i

    def __str__(self) -> str:
        return "{}".format(self.i)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.i == other.i


class Symbol(Token):
    def __init__(self, s: str):
        self.token_type = TokenType.SYMBOL
        self.s = s

    def __str__(self) -> str:
        return self.s

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.s == other.s


class _SpecialToken:
    def __init__(self, token_type: TokenType, ch: str):
        self.token_type = token_type
        self.ch = ch

    def __str__(self):
        return self.ch


LParen = _SpecialToken(TokenType.LPAREN, "(")
RParen = _SpecialToken(TokenType.RPAREN, ")")


class TokenError(Exception):
    def __init__(self, ch: str):
        super().__init__("unexpected charactor: {}".format(ch))


def tokenize(program: str) -> List[Token]:
    program2 = program.replace("(", " ( ").replace(")", " ) ")
    words = program2.split(" ")

    tokens: List[Token] = []
    for word in words:
        if word in ["", "\n"]:
            continue

        if word == "(":
            tokens.append(LParen)
        elif word == ")":
            tokens.append(RParen)
        else:
            try:
                i = int(word)
                tokens.append(Integer(i))
            except ValueError:
                tokens.append(Symbol(word))

    return tokens
