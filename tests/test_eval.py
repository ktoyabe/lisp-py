from lisp import leval, lexer, parser, lobject, env


def eval_program(program: str):
    environment = env.new()
    tokens = lexer.tokenize(program)
    o = parser.parse(tokens)
    result = leval.evaluate(o, environment)
    return result


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


def test_string_concat():
    assert eval_program('(+ "Hello" " World")') == lobject.String("Hello World")


def test_string_eq():
    assert eval_program('(= "ab c" "ab c")') == lobject.Bool(True)
    assert eval_program('(= "ab c" "def")') == lobject.Bool(False)


def test_string_ne():
    assert eval_program('(!= "ab c" "ab c")') == lobject.Bool(False)
    assert eval_program('(!= "ab c" "def")') == lobject.Bool(True)


def test_string_less():
    assert eval_program('(< "ab c" "ab b")') == lobject.Bool(False)
    assert eval_program('(< "ab c" "ab c")') == lobject.Bool(False)
    assert eval_program('(< "ab c" "ab d")') == lobject.Bool(True)


def test_string_greter():
    assert eval_program('(> "ab c" "ab b")') == lobject.Bool(True)
    assert eval_program('(> "ab c" "ab c")') == lobject.Bool(False)
    assert eval_program('(> "ab c" "ab d")') == lobject.Bool(False)


def test_float_add():
    assert eval_program("(+ 3.14 5.0)") == lobject.Float(8.14)


def test_float_sub():
    assert eval_program("(- 3.14 5.0)") == lobject.Float(3.14 - 5.0)


def test_float_mul():
    assert eval_program("(* 3.14 5.0)") == lobject.Float(3.14 * 5.0)


def test_float_div():
    assert eval_program("(/ 3.14 5.0)") == lobject.Float(3.14 / 5.0)


def test_factorial():
    program = """(
        (define fact (lambda (n) (if (< n 1) 1 (* n (fact (- n 1))))))
        (fact 5)
    )"""

    result = eval_program(program)
    assert result == lobject.LList([lobject.Integer(120)])


def test_list_data():
    program = "(if #t (list 1 2 3) (list 4 5))"
    assert eval_program(program) == lobject.ListData(
        [lobject.Integer(1), lobject.Integer(2), lobject.Integer(3)]
    )


def test_list_data_add():
    program = "(+ (list 1) (list 3 2))"
    assert eval_program(program) == lobject.ListData(
        [lobject.Integer(1), lobject.Integer(3), lobject.Integer(2)]
    )


def test_map():
    program = """(
        (define sqr (lambda (r) (* r r)))
        (define l (list 1 2 3))
        (map sqr l)
    )
    """
    result = eval_program(program)
    assert result == lobject.LList(
        [
            lobject.ListData(
                [
                    lobject.Integer(1),
                    lobject.Integer(4),
                    lobject.Integer(9),
                ]
            )
        ]
    )


def test_filter():
    program = """(
        (define odd (lambda (x) (= 1 (% x 2))))
        (define l (list 1 2 3 4 5))
        (filter odd l)
    )
    """
    result = eval_program(program)
    assert result == lobject.LList(
        [
            lobject.ListData(
                [
                    lobject.Integer(1),
                    lobject.Integer(3),
                    lobject.Integer(5),
                ]
            )
        ]
    )
