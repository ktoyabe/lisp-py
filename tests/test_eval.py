from lisp import leval, lexer, parser, lobject, env


def eval_program(program: str):
    environment = env.new()
    tokens = lexer.tokenize(program)
    o = parser.parse(tokens)
    return leval.evaluate(o, environment)


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
    assert result == lobject.LList([lobject.Integer(314 * 10 * 10)])


def test_sqr_function():
    program = """(
        (define sqr (lambda (r) (* r r)))
        (sqr 10)
    )"""
    result = eval_program(program)
    assert result == lobject.LList([lobject.Integer(10 * 10)])


def test_bool():
    assert eval_program("(< 1 2)") == lobject.Bool(True)
    assert eval_program("(> 1 2)") == lobject.Bool(False)
    assert eval_program("(= 1 2)") == lobject.Bool(False)
    assert eval_program("(!= 1 2)") == lobject.Bool(True)


def test_bool_constants():
    eval_program("(if (< 1 2) #t #f)") == lobject.Bool(True)
    eval_program("(if (> 1 2) #t #f)") == lobject.Bool(False)
    eval_program("(if (> 1 2) #t #nil)") == lobject.Void


def test_if():
    assert eval_program("(if (< 1 2) 1 2)") == lobject.Integer(1)
    assert eval_program("(if (> 1 2) 1 2)") == lobject.Integer(2)


def test_string():
    program = '(if (< 1 2) "foo bar" "hoge hoge")'
    assert eval_program(program) == lobject.String("foo bar")


def test_string_op():
    assert eval_program('(+ "Hello" " World")') == lobject.String("Hello World")
    assert eval_program('(< "abc" "def")') == lobject.Bool(True)
    assert eval_program('(> "abc" "def")') == lobject.Bool(False)
    assert eval_program('(= "abc" "def")') == lobject.Bool(False)
    assert eval_program('(!= "abc" "def")') == lobject.Bool(True)


def test_factorial():
    program = """(
        (define fact (lambda (n) (if (< n 1) 1 (* n (fact (- n 1))))))
        (fact 5)
    )"""

    result = eval_program(program)
    assert result == lobject.LList([lobject.Integer(120)])
