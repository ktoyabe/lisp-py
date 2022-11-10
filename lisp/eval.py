from typing import List
from lisp import lobject


class EvalError(Exception):
    pass


def eval(o: lobject.Object):
    return _eval_obj(o)


def _eval_obj(o: lobject.Object):
    if o.object_type == lobject.ObjectType.LIST:
        return _eval_list(o.l)
    elif o.object_type == lobject.ObjectType.VOID:
        return lobject.Void
    elif o.object_type == lobject.ObjectType.LAMBDA:
        raise NotImplementedError("eval lambda is not implemented")
    elif o.object_type == lobject.ObjectType.BOOL:
        raise NotImplementedError("eval bool is not implemented")
    elif o.object_type == lobject.ObjectType.INTEGER:
        return lobject.Integer(o.i)
    elif o.object_type == lobject.ObjectType.SYMBOL:
        return lobject.Symbol(o.s)
    else:
        raise EvalError("unknown object type. object_type={}".format(o.object_type))


def _eval_list(l: List[lobject.List]):
    head = l[0]
    if head.object_type == lobject.ObjectType.SYMBOL:
        if head.s in ["+", "-", "*", "/", "<", ">", "=", "!="]:
            return _eval_binary_op(l)
    else:
        raise NotImplementedError("_eval_list not implemented yet")


def _eval_binary_op(l: List[lobject.List]):
    if len(l) != 3:
        raise EvalError(
            "Invalid number of arguments for infix operator. len={}", len(l)
        )

    op = l[0].s
    left = l[1]
    right = l[2]

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
