from abc import ABC
from typing import List, Optional


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


class TokenError(Exception):
    def __init__(self, err: str):
        super().__init__("Tokenization error: {}".format(err))


def tokenize(program: str) -> List[Token]:
    tokens: List[Token] = []
    chars = list(program)

    if len(chars) == 0:
        return tokens

    while len(chars) > 0:
        ch = chars.pop(0)
        if ch == "(":
            tokens.append(LParen)
        elif ch == ")":
            tokens.append(RParen)
        elif ch == '"':
            # read string
            word_buf = []
            while len(chars) > 0 and chars[0] != '"':
                word_buf.append(chars.pop(0))

            if len(chars) > 0 and chars[0] == '"':
                chars.pop(0)
            else:
                raise TokenError("Unterminated string: {}".format("".join(word_buf)))

            word = "".join(word_buf)
            tokens.append(String(word))
        else:
            word_buf = []
            while len(chars) > 0 and not _is_whitespace(ch) and ch != "(" and ch != ")":
                word_buf.append(ch)
                peek = chars[0]
                if peek == "(" or peek == ")":
                    break

                ch = chars.pop(0)

            if len(word_buf) == 0:
                continue

            word = "".join(word_buf)

            i = _parse_int(word)
            if i is not None:
                tokens.append(Integer(i))
                continue

            f = _parse_float(word)
            if f is not None:
                tokens.append(Float(f))
                continue

            if word in [
                "define",
                "list",
                "print",
                "lambda",
                "map",
                "filter",
                "reduce",
                "length",
                "range",
            ]:
                tokens.append(Keyword(word))
            elif word == "if":
                tokens.append(If)
            elif word in ["+", "-", "*", "/", "%", "<", ">", "=", "!="]:
                tokens.append(BinaryOp(word))
            else:
                tokens.append(Symbol(word))

    return tokens


def _is_whitespace(ch: str) -> bool:
    return ch in [" ", "\t", "\n", "\r"]


def _parse_int(word: str) -> Optional[int]:
    try:
        return int(word)
    except ValueError:
        return None


def _parse_float(word: str) -> Optional[float]:
    try:
        return float(word)
    except ValueError:
        return None
