from typing import List
from lisp import lobject, env


class EvalError(Exception):
    pass


def eval(o: lobject.Object, environment: env.Env):
    return _eval_obj(o, environment)


def _eval_symbol(s: str, environment: env.Env) -> lobject.Object:
    val = environment.get(s)
    if val is None:
        raise EvalError("Unbound symbol: {}".format(s))

    return val


def _eval_obj(o: lobject.Object, environment: env.Env):
    if o.object_type == lobject.ObjectType.LIST:
        return _eval_list(o.l, environment)
    elif o.object_type == lobject.ObjectType.VOID:
        return lobject.Void
    elif o.object_type == lobject.ObjectType.LAMBDA:
        raise NotImplementedError("eval lambda is not implemented")
    elif o.object_type == lobject.ObjectType.BOOL:
        raise NotImplementedError("eval bool is not implemented")
    elif o.object_type == lobject.ObjectType.INTEGER:
        return lobject.Integer(o.i)
    elif o.object_type == lobject.ObjectType.SYMBOL:
        return _eval_symbol(o.s, environment)
    else:
        raise EvalError("unknown object type. object_type={}".format(o.object_type))


def _eval_define(l: List[lobject.List], environment: env.Env) -> lobject.Object:
    if len(l) != 3:
        raise EvalError("Invalid number of arguments for define")

    if l[1].object_type != lobject.ObjectType.SYMBOL:
        raise EvalError("Invalid define")
    sym = l[1].s

    val = _eval_obj(l[2], env)
    environment.set(sym, val)

    return lobject.Void


def _eval_function_def(l: List[lobject.List], environment: env.Env) -> lobject.Object:
    # parse parameters
    if l[1].object_type != lobject.ObjectType.LIST:
        raise EvalError('Invalid lambda parameter. "{}"'.format(l[1]))
    params: List[str] = []
    for param in l[1].l:
        if param.object_type != lobject.ObjectType.SYMBOL:
            raise EvalError('Invalid lambda parameter. "{}"'.format(param))
        params.append(param.s)

    # parse body
    if l[2].object_type != lobject.ObjectType.LIST:
        raise EvalError("Invalid lambda. body must be lobject.List")
    return lobject.Lambda(params, l[2].l.copy())


def _eval_function_call(
    sym: str, l: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    lambda_obj = environment.get(sym)
    if lambda_obj is None:
        raise EvalError("Unbound symbol: {}".format(sym))
    if lambda_obj.object_type != lobject.ObjectType.LAMBDA:
        raise EvalError("Not a lambda. object_type={}".format(lambda_obj.object_type))

    params: List[str] = lambda_obj.params
    body = lambda_obj.body
    new_env = env.extend(environment)

    for i, param in enumerate(params):
        # i + 1 => skip function name when function call.
        # ex)  function def : (define sqr (r) (* r r)) ---> r index is 0
        #      function call: (sqr 10) ---> i + 1 (0 + 1) is 10
        val = _eval_obj(l[i + 1], env)
        new_env.set(param, val)

    return _eval_obj(lobject.List(body), new_env)


def _eval_list(l: List[lobject.List], environment: env.Env):
    head = l[0]
    if head.object_type == lobject.ObjectType.SYMBOL:
        if head.s in ["+", "-", "*", "/", "<", ">", "=", "!="]:
            return _eval_binary_op(l, environment)
        elif head.s == "define":
            return _eval_define(l, environment)
        elif head.s == "lambda":
            return _eval_function_def(l, environment)
        else:
            return _eval_function_call(head.s, l, environment)
    else:
        new_list: List[lobject.Object] = []
        for obj in l:
            result = _eval_obj(obj, environment)
            if result.object_type == lobject.ObjectType.VOID:
                pass
            else:
                new_list.append(result)
        return lobject.List(new_list)


def _eval_binary_op(l: List[lobject.List], environment: env.Env):
    if len(l) != 3:
        raise EvalError(
            "Invalid number of arguments for infix operator. len={}", len(l)
        )

    op = l[0].s
    left = _eval_obj(l[1], environment)
    right = _eval_obj(l[2], environment)

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
        return lobject.Integer(left.i < right.i)
    elif op == ">":
        return lobject.Integer(left.i > right.i)
    elif op == "=":
        return lobject.Integer(left.i == right.i)
    elif op == "!=":
        return lobject.Integer(left.i != right.i)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))
