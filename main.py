from lisp import leval, lexer, parser, env, lobject

PROMPT = "lisp-py> "


def _eval_program(program: str, environment: env.Env):
    tokens = lexer.tokenize(program)
    ast = parser.parse(tokens)
    return leval.evaluate(ast, environment)


def main():
    environment = env.new()

    while True:
        print(PROMPT, end="")
        line = input()
        if line == "exit":
            break

        val = _eval_program(line, environment)
        if val.object_type == lobject.ObjectType.VOID:
            pass
        elif val.object_type == lobject.ObjectType.INTEGER:
            print("{}".format(val.i))
        elif val.object_type == lobject.ObjectType.BOOL:
            print("{}".format(val.b))
        elif val.object_type == lobject.ObjectType.SYMBOL:
            print("{}".format(val.s))
        elif val.object_type == lobject.ObjectType.LAMBDA:
            print("Lambda(", end="")
            for param in val.params:
                print("{} ".format(param), end="")
            print(")", end="")
            for expr in val.body:
                print(" {}".format(expr), end="")
            print("")
        else:
            return print("{}".format(val))


if __name__ == "__main__":
    main()
