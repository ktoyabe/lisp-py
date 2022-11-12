from abc import ABC


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


class Float(Token):
    def __init__(self, f: float):
        self.f = f

    def __str__(self) -> str:
        return "{}".format(self.f)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Float):
            return False
        return self.f == other.f


class Symbol(Token):
    def __init__(self, s: str):
        self.s = s

    def __str__(self) -> str:
        return self.s

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Symbol):
            return False
        return self.s == other.s


class String(Token):
    def __init__(self, string: str):
        self.string = string

    def __str__(self) -> str:
        return self.string

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, String):
            return False
        return self.string == other.string


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
If = _SpecialToken("if")


class Keyword(Token):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Keyword):
            return False

        return self.keyword == other.keyword

    def __str__(self) -> str:
        return self.keyword


class BinaryOp(Token):
    def __init__(self, op: str):
        self.op = op

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, BinaryOp):
            return False

        return self.op == other.op

    def __str__(self) -> str:
        return self.op
