from abc import ABC
from enum import IntEnum, auto
from typing import List


class TokenType(IntEnum):
    INTEGER = auto()
    SYMBOL = auto()
    LPAREN = auto()
    RPAREN = auto()


class Token(ABC):
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class Integer(Token):
    def __init__(self, i: int):
        self.i = i

    def __str__(self) -> str:
        return "{}".format(self.i)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Integer):
            return False
        return self.i == other.i


class Symbol(Token):
    def __init__(self, s: str):
        self.s = s

    def __str__(self) -> str:
        return self.s

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Symbol):
            return False
        return self.s == other.s


class _SpecialToken(Token):
    def __init__(self, ch: str):
        self.ch = ch

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, _SpecialToken):
            return False

        return self.ch == other.ch

    def __str__(self) -> str:
        return self.ch


LParen = _SpecialToken("(")
RParen = _SpecialToken(")")


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
