from typing import List, Optional

from lisp import token


class TokenError(Exception):
    def __init__(self, err: str):
        super().__init__("Tokenization error: {}".format(err))


def tokenize(program: str) -> List[token.Token]:
    tokens: List[token.Token] = []
    chars = list(program)

    if len(chars) == 0:
        return tokens

    while len(chars) > 0:
        ch = chars.pop(0)
        if ch == "(":
            tokens.append(token.LParen)
        elif ch == ")":
            tokens.append(token.RParen)
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
            tokens.append(token.String(word))
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
                tokens.append(token.Integer(i))
                continue

            f = _parse_float(word)
            if f is not None:
                tokens.append(token.Float(f))
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
                tokens.append(token.Keyword(word))
            elif word == "if":
                tokens.append(token.If)
            elif word in ["+", "-", "*", "/", "%", "<", ">", "=", "!="]:
                tokens.append(token.BinaryOp(word))
            else:
                tokens.append(token.Symbol(word))

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
