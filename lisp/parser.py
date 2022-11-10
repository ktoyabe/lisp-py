from typing import List

from lisp import lobject
from lisp import token


class ParseError(Exception):
    def __init__(self, err: str):
        super().__init__("Parse error: {}".format(err))


def _parse_list(tokens: List[token.Token]):
    lobject.Object

    t = tokens.pop(-1)
    if t != token.LParen:
        raise ParseError("Expected LParen, found {}".format(t))

    objects: List[lobject.Object] = []
    while len(tokens) != 0:
        t = tokens.pop(-1)

        if t.token_type == token.TokenType.INTEGER:
            objects.append(lobject.Integer(t.i))
        elif t.token_type == token.TokenType.SYMBOL:
            objects.append(lobject.Symbol(t.s))
        elif t.token_type == token.TokenType.LPAREN:
            tokens.append(token.LParen)
            sub_list = _parse_list(tokens)
            objects.append(sub_list)
        elif t.token_type == token.TokenType.RPAREN:
            return lobject.List(objects)

    return lobject.List(objects)


def parse(tokens: List[token.Token]):
    lobject.Object

    if len(tokens) == 0:
        raise ParseError("tokens are empty.")

    ts = tokens.copy()
    ts.reverse()

    return _parse_list(ts)
