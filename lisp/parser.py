from typing import List

from lisp import lobject, token
from lisp.token import TokenType


class ParseError(Exception):
    def __init__(self, err: str):
        super().__init__("Parse error: {}".format(err))


def _parse_list(tokens: List[token.Token]) -> lobject.Object:
    t = tokens.pop(-1)
    if t.token_type != TokenType.LPAREN:
        raise ParseError("Expected LParen, found {}".format(t))

    objects: List[lobject.Object] = []
    while len(tokens) != 0:
        t = tokens.pop(-1)

        if t.token_type == TokenType.INT:
            objects.append(lobject.Integer(int(t.literal)))
        elif t.token_type == TokenType.FLOAT:
            objects.append(lobject.Float(float(t.literal)))
        elif t.token_type == TokenType.KEYWORD:
            objects.append(lobject.Keyword(t.literal))
        elif t.token_type == TokenType.IF:
            objects.append(lobject.If)
        elif t.token_type == TokenType.BINARY_OP:
            objects.append(lobject.BinaryOp(t.literal))
        elif t.token_type == TokenType.SYMBOL:
            objects.append(lobject.Symbol(t.literal))
        elif t.token_type == TokenType.STRING:
            objects.append(lobject.String(t.literal))
        elif t.token_type == TokenType.LPAREN:
            tokens.append(token.Token(TokenType.LPAREN, "("))
            sub_list = _parse_list(tokens)
            objects.append(sub_list)
        elif t.token_type == TokenType.RPAREN:
            return lobject.LList(objects)

    return lobject.LList(objects)


def parse(tokens: List[token.Token]) -> lobject.Object:
    if len(tokens) == 0:
        raise ParseError("tokens are empty.")

    ts = tokens.copy()
    ts.reverse()

    return _parse_list(ts)
