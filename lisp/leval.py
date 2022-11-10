from typing import List
from lisp import lobject, env


class EvalError(Exception):
    pass


def evaluate(o: lobject.Object, environment: env.Env):
    return _eval_obj(o, environment)


def _eval_symbol(s: str, environment: env.Env) -> lobject.Object:
    val = environment.get(s)
    if val is None:
        raise EvalError("Unbound symbol: {}".format(s))

    return val


def _eval_obj(o: lobject.Object, environment: env.Env) -> lobject.Object:
    if isinstance(o, lobject.LList):
        return _eval_list(o.object_list, environment)
    elif o == lobject.Void:
        return lobject.Void
    elif isinstance(o, lobject.Lambda):
        raise NotImplementedError("eval lambda is not implemented")
    elif isinstance(o, lobject.Bool):
        raise NotImplementedError("eval bool is not implemented")
    elif isinstance(o, lobject.Integer):
        return lobject.Integer(o.i)
    elif isinstance(o, lobject.Symbol):
        return _eval_symbol(o.s, environment)
    else:
        raise EvalError("unknown object type. object_type={}".format(type(o)))


def _eval_define(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 3:
        raise EvalError("Invalid number of arguments for define")

    if not isinstance(object_list[1], lobject.Symbol):
        raise EvalError("Invalid define")
    sym = object_list[1].s

    val = _eval_obj(object_list[2], environment)
    environment.set(sym, val)

    return lobject.Void


def _eval_function_def(object_list: List[lobject.Object]) -> lobject.Object:
    # parse parameters
    if not isinstance(object_list[1], lobject.LList):
        raise EvalError('Invalid lambda parameter. "{}"'.format(object_list[1]))
    params: List[str] = []
    for param in object_list[1].object_list:
        if not isinstance(param, lobject.Symbol):
            raise EvalError('Invalid lambda parameter. "{}"'.format(param))
        params.append(param.s)

    # parse body
    if not isinstance(object_list[2], lobject.LList):
        raise EvalError("Invalid lambda. body must be lobject.LList")
    return lobject.Lambda(params, object_list[2].object_list.copy())


def _eval_function_call(
    sym: str, object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    lambda_obj = environment.get(sym)
    if lambda_obj is None:
        raise EvalError("Unbound symbol: {}".format(sym))
    if not isinstance(lambda_obj, lobject.Lambda):
        raise EvalError("Not a lambda. object_type={}".format(type(lambda_obj)))

    params: List[str] = lambda_obj.params
    body = lambda_obj.body
    new_env = env.extend(environment)

    for i, param in enumerate(params):
        # i + 1 => skip function name when function call.
        # ex)  function def : (define sqr (r) (* r r)) ---> r index is 0
        #      function call: (sqr 10) ---> i + 1 (0 + 1) is 10
        val = _eval_obj(object_list[i + 1], environment)
        new_env.set(param, val)

    return _eval_obj(lobject.LList(body), new_env)


def _eval_if(object_list: List[lobject.Object], environment: env.Env) -> lobject.Object:
    if len(object_list) != 4:
        raise EvalError("Invalid number of arguments for if statement")

    cond_obj = _eval_obj(object_list[1], environment)
    if not isinstance(cond_obj, lobject.Bool):
        raise EvalError("Condition must be a boolean. actual={}".format(cond_obj))

    if cond_obj.b:
        return _eval_obj(object_list[2], environment)
    else:
        return _eval_obj(object_list[3], environment)


def _eval_list(object_list: List[lobject.Object], environment: env.Env):
    head = object_list[0]
    if isinstance(head, lobject.Symbol):
        if head.s in ["+", "-", "*", "/", "<", ">", "=", "!="]:
            return _eval_binary_op(object_list, environment)
        elif head.s == "define":
            return _eval_define(object_list, environment)
        elif head.s == "lambda":
            return _eval_function_def(object_list)
        elif head.s == "if":
            return _eval_if(object_list, environment)
        else:
            return _eval_function_call(head.s, object_list, environment)
    else:
        new_list: List[lobject.Object] = []
        for obj in object_list:
            result = _eval_obj(obj, environment)
            if result == lobject.Void:
                pass
            else:
                new_list.append(result)
        return lobject.LList(new_list)


def _eval_binary_op(object_list: List[lobject.Object], environment: env.Env):
    if len(object_list) != 3:
        raise EvalError(
            "Invalid number of arguments for infix operator. len={}".format(
                len(object_list)
            )
        )
    if not isinstance(object_list[0], lobject.Symbol):
        raise EvalError("Operator must be Symbol. {}".format(object_list[0]))

    op = object_list[0].s
    left = _eval_obj(object_list[1], environment)
    right = _eval_obj(object_list[2], environment)

    if type(left) != lobject.Integer:
        raise EvalError("Left operand must be an integer {}".format(left))

    if type(right) != lobject.Integer:
        raise EvalError("Right operand must be an integer {}".format(right))

    if op == "+":
        return lobject.Integer(left.i + right.i)
    elif op == "-":
        return lobject.Integer(left.i - right.i)
    elif op == "*":
        return lobject.Integer(left.i * right.i)
    elif op == "/":
        return lobject.Integer(left.i // right.i)
    elif op == "<":
        return lobject.Bool(left.i < right.i)
    elif op == ">":
        return lobject.Bool(left.i > right.i)
    elif op == "=":
        return lobject.Bool(left.i == right.i)
    elif op == "!=":
        return lobject.Bool(left.i != right.i)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))
