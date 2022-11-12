from typing import List

from lisp import lobject, token


class ParseError(Exception):
    def __init__(self, err: str):
        super().__init__("Parse error: {}".format(err))


def _parse_list(tokens: List[token.Token]) -> lobject.Object:
    t = tokens.pop(-1)
    if t != token.LParen:
        raise ParseError("Expected LParen, found {}".format(t))

    objects: List[lobject.Object] = []
    while len(tokens) != 0:
        t = tokens.pop(-1)

        if isinstance(t, token.Integer):
            objects.append(lobject.Integer(t.i))
        elif isinstance(t, token.Float):
            objects.append(lobject.Float(t.f))
        elif isinstance(t, token.Keyword):
            objects.append(lobject.Keyword(t.keyword))
        elif t == token.If:
            objects.append(lobject.If)
        elif isinstance(t, token.BinaryOp):
            objects.append(lobject.BinaryOp(t.op))
        elif isinstance(t, token.Symbol):
            objects.append(lobject.Symbol(t.s))
        elif isinstance(t, token.String):
            objects.append(lobject.String(t.string))
        elif t == token.LParen:
            tokens.append(token.LParen)
            sub_list = _parse_list(tokens)
            objects.append(sub_list)
        elif t == token.RParen:
            return lobject.LList(objects)

    return lobject.LList(objects)


def parse(tokens: List[token.Token]) -> lobject.Object:
    if len(tokens) == 0:
        raise ParseError("tokens are empty.")

    ts = tokens.copy()
    ts.reverse()

    return _parse_list(ts)
