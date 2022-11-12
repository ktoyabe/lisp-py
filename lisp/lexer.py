from typing import List, Optional

from lisp.token import Token, TokenType


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
            tokens.append(Token(TokenType.LPAREN, ch))
        elif ch == ")":
            tokens.append(Token(TokenType.RPAREN, ch))
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
            tokens.append(Token(TokenType.STRING, word))
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
                tokens.append(Token(TokenType.INT, word))
                continue

            f = _parse_float(word)
            if f is not None:
                tokens.append(Token(TokenType.FLOAT, word))
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
                tokens.append(Token(TokenType.KEYWORD, word))
            elif word == "if":
                tokens.append(Token(TokenType.IF, word))
            elif word in ["+", "-", "*", "/", "%", "<", ">", "=", "!="]:
                tokens.append(Token(TokenType.BINARY_OP, word))
            else:
                tokens.append(Token(TokenType.SYMBOL, word))

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
