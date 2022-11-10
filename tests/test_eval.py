from lisp import token, parser, lobject, eval, env


def eval_program(program: str):
    environment = env.new()
    tokens = token.tokenize(program)
    o = parser.parse(tokens)
    return eval.eval(o, environment)


def test_simple_add():
    o = eval_program("(+ 1 2)")

    assert o == lobject.Integer(3)


def test_area_of_circle():
    program = """(
        (define r 10)
        (* 314 (* r r))
    )
    """
    result = eval_program(program)
    assert result == lobject.List([lobject.Integer(314 * 10 * 10)])


def test_sqr_function():
    program = """(
        (define sqr (lambda (r) (* r r)))
        (sqr 10)
    )"""
    result = eval_program(program)
    assert result == lobject.List([lobject.Integer(10 * 10)])
