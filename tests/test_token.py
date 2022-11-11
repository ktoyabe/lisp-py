from lisp import lexer


def test_add():
    tokens = lexer.tokenize("(+ 1 2)")
    assert tokens == [
        lexer.LParen,
        lexer.BinaryOp("+"),
        lexer.Integer(1),
        lexer.Integer(2),
        lexer.RParen,
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
        lexer.LParen,
        lexer.LParen,
        lexer.Keyword("define"),
        lexer.Symbol("r"),
        lexer.Integer(10),
        lexer.RParen,
        lexer.LParen,
        lexer.BinaryOp("*"),
        lexer.Symbol("pi"),
        lexer.LParen,
        lexer.BinaryOp("*"),
        lexer.Symbol("r"),
        lexer.Symbol("r"),
        lexer.RParen,
        lexer.RParen,
        lexer.RParen,
    ]


def test_string():
    program = '(define str "Hello World")'
    tokens = lexer.tokenize(program)
    assert tokens == [
        lexer.LParen,
        lexer.Keyword("define"),
        lexer.Symbol("str"),
        lexer.String("Hello World"),
        lexer.RParen,
    ]


def test_float():
    program = "(define pi 3.14)"
    tokens = lexer.tokenize(program)
    assert tokens == [
        lexer.LParen,
        lexer.Keyword("define"),
        lexer.Symbol("pi"),
        lexer.Float(3.14),
        lexer.RParen,
    ]
