from lisp import lexer
from lisp.token import Token, TokenType


def test_add():
    tokens = lexer.tokenize("(+ 1 2)")
    assert tokens == [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.BINARY_OP, "+"),
        Token(TokenType.INT, "1"),
        Token(TokenType.INT, "2"),
        Token(TokenType.RPAREN, ")"),
    ]


def test_area_of_circle():
    program = """
        (
            (define r 10)
            (* pi (* r r))
        )
    """
    tokens = lexer.tokenize(program)

    assert tokens == [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.KEYWORD, "define"),
        Token(TokenType.SYMBOL, "r"),
        Token(TokenType.INT, "10"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.BINARY_OP, "*"),
        Token(TokenType.SYMBOL, "pi"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.BINARY_OP, "*"),
        Token(TokenType.SYMBOL, "r"),
        Token(TokenType.SYMBOL, "r"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.RPAREN, ")"),
    ]


def test_string():
    program = '(define str "Hello World")'
    tokens = lexer.tokenize(program)
    assert tokens == [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.KEYWORD, "define"),
        Token(TokenType.SYMBOL, "str"),
        Token(TokenType.STRING, "Hello World"),
        Token(TokenType.RPAREN, ")"),
    ]


def test_float():
    program = "(define pi 3.14)"
    tokens = lexer.tokenize(program)
    assert tokens == [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.KEYWORD, "define"),
        Token(TokenType.SYMBOL, "pi"),
        Token(TokenType.FLOAT, "3.14"),
        Token(TokenType.RPAREN, ")"),
    ]
