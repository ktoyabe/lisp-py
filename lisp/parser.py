from typing import List

from lisp import lobject
from lisp import token


class ParseError(Exception):
    def __init__(self, err: str):
        super().__init__("Parse error: {}".format(err))


def parse(tokens: List[token.Token]):
    List[lobject.Object]

    if len(tokens) == 0:
        raise ParseError("tokens are empty.")

    t = tokens.pop(0)
    if t != token.LParen:
        raise ParseError("Expected LParen, found {}".format(t))

    objects: List[lobject.Object] = []
    while len(tokens) != 0:
        t = tokens.pop(0)

        if t.token_type == token.TokenType.INTEGER:
            objects.append(lobject.Integer(t.i))
        elif t.token_type == token.TokenType.SYMBOL:
            objects.append(lobject.Symbol(t.s))
        elif t.token_type == token.TokenType.RPAREN:
            return lobject.List(objects)

    return lobject.List(objects)
