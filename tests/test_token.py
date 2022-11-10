from lisp import lexer


def test_add():
    tokens = lexer.tokenize("(+ 1 2)")
    assert tokens == [
        lexer.LParen,
        lexer.Symbol("+"),
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
        lexer.Symbol("define"),
        lexer.Symbol("r"),
        lexer.Integer(10),
        lexer.RParen,
        lexer.LParen,
        lexer.Symbol("*"),
        lexer.Symbol("pi"),
        lexer.LParen,
        lexer.Symbol("*"),
        lexer.Symbol("r"),
        lexer.Symbol("r"),
        lexer.RParen,
        lexer.RParen,
        lexer.RParen,
    ]
