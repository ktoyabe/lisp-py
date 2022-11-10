from lisp import token, parser, lobject, eval


def eval_program(program: str):
    tokens = token.tokenize(program)
    o = parser.parse(tokens)
    return eval.eval(o)


def test_simple_add():
    o = eval_program("(+ 1 2)")

    assert o == lobject.Integer(3)
