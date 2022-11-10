from lisp import lexer, lobject, parser


def test_add():
    tokens = lexer.tokenize("(+ 1 2)")
    result = parser.parse(tokens)

    assert result == lobject.LList(
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
    tokens = lexer.tokenize(programs)
    result = parser.parse(tokens)
    assert result == lobject.LList(
        [
            lobject.LList(
                [
                    lobject.Symbol("define"),
                    lobject.Symbol("r"),
                    lobject.Integer(10),
                ]
            ),
            lobject.LList(
                [
                    lobject.Symbol("*"),
                    lobject.Symbol("pi"),
                    lobject.LList(
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


def test_area_of_circle_str():
    programs = """(
        (define r 10)
        (* pi (* r r))
    )"""
    tokens = lexer.tokenize(programs)
    result = parser.parse(tokens)
    assert "{}".format(result) == "((define r 10) (* pi (* r r)))"
