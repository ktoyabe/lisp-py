from lisp import token, lexer


def test_add():
    tokens = lexer.tokenize("(+ 1 2)")
    assert tokens == [
        token.LParen,
        token.BinaryOp("+"),
        token.Integer(1),
        token.Integer(2),
        token.RParen,
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
        token.LParen,
        token.LParen,
        token.Keyword("define"),
        token.Symbol("r"),
        token.Integer(10),
        token.RParen,
        token.LParen,
        token.BinaryOp("*"),
        token.Symbol("pi"),
        token.LParen,
        token.BinaryOp("*"),
        token.Symbol("r"),
        token.Symbol("r"),
        token.RParen,
        token.RParen,
        token.RParen,
    ]


def test_string():
    program = '(define str "Hello World")'
    tokens = lexer.tokenize(program)
    assert tokens == [
        token.LParen,
        token.Keyword("define"),
        token.Symbol("str"),
        token.String("Hello World"),
        token.RParen,
    ]


def test_float():
    program = "(define pi 3.14)"
    tokens = lexer.tokenize(program)
    assert tokens == [
        token.LParen,
        token.Keyword("define"),
        token.Symbol("pi"),
        token.Float(3.14),
        token.RParen,
    ]
