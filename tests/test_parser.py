from lisp import token, lobject, parser


def test_add():
    tokens = token.tokenize("(+ 1 2)")
    l = parser.parse(tokens)

    print("".format(l))
    assert type(l) == lobject.List
    assert l == lobject.List(
        [
            lobject.Symbol("+"),
            lobject.Integer(1),
            lobject.Integer(2),
        ]
    )
