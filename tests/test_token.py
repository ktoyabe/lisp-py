from lisp import token


def test_add():
    tokens = token.tokenize("(+ 1 2)")
    assert tokens == [
        token.LParen(),
        token.Symbol("+"),
        token.Integer(1),
        token.Integer(2),
        token.RParen(),
    ]


def test_area_of_circle():
    program = """
        (
            (define r 10)
            (* pi (* r r))
        )
    """
    tokens = token.tokenize(program)
    assert tokens == [
        token.LParen(),
        token.LParen(),
        token.Symbol("define"),
        token.Symbol("r"),
        token.Integer(10),
        token.RParen(),
        token.LParen(),
        token.Symbol("*"),
        token.Symbol("pi"),
        token.LParen(),
        token.Symbol("*"),
        token.Symbol("r"),
        token.Symbol("r"),
        token.RParen(),
        token.RParen(),
        token.RParen(),
    ]
