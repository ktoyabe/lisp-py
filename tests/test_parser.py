from lisp import token, lobject, parser


def test_add():
    tokens = token.tokenize("(+ 1 2)")
    l = parser.parse(tokens)

    assert l == lobject.List(
        [
            lobject.Symbol("+"),
            lobject.Integer(1),
            lobject.Integer(2),
        ]
    )


def test_area_of_circle():
    programs = """(
        (define r 10)
        (* pi (* r r))
    )"""
    tokens = token.tokenize(programs)
    l = parser.parse(tokens)
    assert l == lobject.List(
        [
            lobject.List(
                [
                    lobject.Symbol("define"),
                    lobject.Symbol("r"),
                    lobject.Integer(10),
                ]
            ),
            lobject.List(
                [
                    lobject.Symbol("*"),
                    lobject.Symbol("pi"),
                    lobject.List(
                        [
                            lobject.Symbol("*"),
                            lobject.Symbol("r"),
                            lobject.Symbol("r"),
                        ]
                    ),
                ]
            ),
        ]
    )
