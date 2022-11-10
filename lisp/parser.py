from typing import List

from lisp import lobject
from lisp import lexer


class ParseError(Exception):
    def __init__(self, err: str):
        super().__init__("Parse error: {}".format(err))


def _parse_list(tokens: List[lexer.Token]) -> lobject.Object:
    t = tokens.pop(-1)
    if t != lexer.LParen:
        raise ParseError("Expected LParen, found {}".format(t))

    objects: List[lobject.Object] = []
    while len(tokens) != 0:
        t = tokens.pop(-1)

        if isinstance(t, lexer.Integer):
            objects.append(lobject.Integer(t.i))
        elif isinstance(t, lexer.Symbol):
            objects.append(lobject.Symbol(t.s))
        elif t == lexer.LParen:
            tokens.append(lexer.LParen)
            sub_list = _parse_list(tokens)
            objects.append(sub_list)
        elif t == lexer.RParen:
            return lobject.LList(objects)

    return lobject.LList(objects)


def parse(tokens: List[lexer.Token]) -> lobject.Object:
    if len(tokens) == 0:
        raise ParseError("tokens are empty.")

    ts = tokens.copy()
    ts.reverse()

    return _parse_list(ts)
