from typing import List, Optional, Tuple
from lisp import lobject, env


class EvalError(Exception):
    pass


def evaluate(o: lobject.Object, environment: env.Env):
    return _eval_obj(o, environment)


def _eval_symbol(s: str, environment: env.Env) -> lobject.Object:
    if s == "#t":
        return lobject.Bool(True)
    elif s == "#f":
        return lobject.Bool(False)
    elif s == "#nil":
        return lobject.Void
    else:
        val = environment.get(s)
        if val is None:
            raise EvalError("Unbound symbol: {}".format(s))
        return val


def _eval_keyword(obj_list: List[lobject.Object], environment: env.Env):
    head = obj_list[0]
    if not isinstance(head, lobject.Keyword):
        raise EvalError("Invalid keyword: {}".format(head))
    kw = head.keyword

    if kw == "define":
        return _eval_define(obj_list, environment)
    elif kw == "list":
        return _eval_list_data(obj_list, environment)
    elif kw == "lambda":
        return _eval_function_def(obj_list)
    elif kw == "map":
        return _eval_map(obj_list, environment)
    elif kw == "filter":
        return _eval_filter(obj_list, environment)
    elif kw == "reduce":
        return _eval_reduce(obj_list, environment)
    elif kw == "length":
        return _eval_length(obj_list, environment)
    elif kw == "range":
        return _eval_range(obj_list, environment)
    else:
        raise EvalError("Unbound keyword: {}".format(kw))


def _eval_obj(o: lobject.Object, environment: env.Env) -> lobject.Object:
    current_obj = o
    current_env = environment

    while True:
        if isinstance(current_obj, lobject.LList):
            head = current_obj.object_list[0]
            if isinstance(head, lobject.BinaryOp):
                return _eval_binary_op(current_obj.object_list, current_env)
            elif isinstance(head, lobject.Keyword):
                return _eval_keyword(current_obj.object_list, current_env)
            elif head == lobject.If:
                current_obj = _eval_if_wo_body_eval(current_obj, current_env)
                continue
            elif isinstance(head, lobject.Symbol):
                # TODO: I do not under stand this block.
                lambda_obj = current_env.get(head.s)
                if lambda_obj is None:
                    raise EvalError("Unvound function: {}", head.s)

                if not isinstance(lambda_obj, lobject.Lambda):
                    raise EvalError("Not a lambda")
                new_env = env.extend(current_env)
                for i, param in enumerate(lambda_obj.params):
                    val = _eval_obj(current_obj.object_list[i + 1], current_env)
                    new_env.set(param, val)

                current_obj = lobject.LList(lambda_obj.body)
                current_env = new_env
                continue
            else:
                new_list = []
                for obj in current_obj.object_list:
                    result = _eval_obj(obj, current_env)
                    if result == lobject.Void:
                        pass
                    else:
                        new_list.append(result)
                return lobject.LList(new_list)
        elif current_obj == lobject.Void:
            return lobject.Void
        elif isinstance(current_obj, lobject.Lambda):
            return lobject.Void
        elif isinstance(current_obj, lobject.Bool):
            return lobject.Bool(current_obj.b)
        elif isinstance(current_obj, lobject.Integer):
            return lobject.Integer(current_obj.i)
        elif isinstance(current_obj, lobject.Float):
            return lobject.Float(current_obj.f)
        elif isinstance(current_obj, lobject.Symbol):
            return _eval_symbol(current_obj.s, current_env)
        elif isinstance(current_obj, lobject.String):
            return lobject.String(current_obj.string)
        elif isinstance(current_obj, lobject.ListData):
            return lobject.ListData(current_obj.list_data)
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


def _eval_if_wo_body_eval(
    current_obj: lobject.LList, current_env: env.Env
) -> lobject.Object:
    if len(current_obj.object_list) != 4:
        raise EvalError("Invalid number of arguments for if statement")

    cond_obj = _eval_obj(current_obj.object_list[1], current_env)
    if not isinstance(cond_obj, lobject.Bool):
        raise EvalError("Condition must be a boolean")
    cond = cond_obj.b

    if cond is True:
        return current_obj.object_list[2]
    else:
        return current_obj.object_list[3]


def _eval_list_data(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    # object_list[0] is "list",

    new_list = []
    for obj in object_list[1:]:
        new_list.append(_eval_obj(obj, environment))
    return lobject.ListData(new_list)


def _is_valid_lambda(
    lambda_obj: lobject.Object, valid_num_params: int
) -> Tuple[bool, Optional[str]]:
    if not isinstance(lambda_obj, lobject.Lambda):
        return (False, "Not a lambda while evaluating map: {}".format(lambda_obj))
    if len(lambda_obj.params) != valid_num_params:
        return (
            False,
            "Invalid number of parameters for lambda function: {}".format(
                lambda_obj.params
            ),
        )
    return (True, None)


def _eval_map(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 3:
        raise EvalError("Invalid number of arguments for map {}".format(object_list))

    # check lambda object
    lambda_obj = _eval_obj(object_list[1], environment)
    ok, err = _is_valid_lambda(lambda_obj, valid_num_params=1)
    if not ok:
        raise EvalError(err)

    # check arg_list
    arg_list = _eval_obj(object_list[2], environment)
    if not isinstance(arg_list, lobject.ListData):
        raise EvalError("Invalid map arguments: {}".format(arg_list))

    func_param = lambda_obj.params[0]  # type: ignore
    result_list: List[lobject.Object] = []
    for arg in arg_list.list_data:
        val = _eval_obj(arg, environment)
        new_env = env.extend(environment)
        new_env.set(func_param, val)
        result = _eval_obj(lobject.LList(lambda_obj.body), new_env)  # type: ignore
        result_list.append(result)
    return lobject.ListData(result_list)


def _eval_filter(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 3:
        raise EvalError("Invalid number of arguments for filter {}".format(object_list))

    # check lambda object
    lambda_obj = _eval_obj(object_list[1], environment)
    ok, err = _is_valid_lambda(lambda_obj, valid_num_params=1)

    # check arg_list
    arg_list = _eval_obj(object_list[2], environment)
    if not isinstance(arg_list, lobject.ListData):
        raise EvalError("Invalid filter arguments: {}".format(arg_list))

    func_param = lambda_obj.params[0]  # type: ignore
    result_list: List[lobject.Object] = []
    for arg in arg_list.list_data:
        val = _eval_obj(arg, environment)
        new_env = env.extend(environment)
        new_env.set(func_param, val)
        result = _eval_obj(lobject.LList(lambda_obj.body), new_env)  # type: ignore

        if not isinstance(result, lobject.Bool):
            raise EvalError("Invalid fitler result: {}".format(result))

        if result.b:
            result_list.append(val)

    return lobject.ListData(result_list)


def _eval_reduce(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 3:
        raise EvalError("Invalid number of arguments for reduce {}".format(object_list))

    # check lambda object
    lambda_obj = _eval_obj(object_list[1], environment)
    ok, err = _is_valid_lambda(lambda_obj, valid_num_params=2)

    # check arg_list
    arg_list = _eval_obj(object_list[2], environment)
    if not isinstance(arg_list, lobject.ListData):
        raise EvalError("Invalid filter arguments: {}".format(arg_list))

    reduce_param1 = lambda_obj.params[0]  # type: ignore
    reduce_param2 = lambda_obj.params[1]  # type: ignore

    accumulator = _eval_obj(arg_list.list_data[0], environment)

    for arg in arg_list.list_data[1:]:
        new_env = env.extend(environment)
        new_env.set(reduce_param1, accumulator)

        val = _eval_obj(arg, environment)
        new_env.set(reduce_param2, val)

        accumulator = _eval_obj(lobject.LList(lambda_obj.body), new_env)  # type: ignore

    return accumulator


def _eval_length(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 2:
        raise EvalError("Invalid number of arguments for length {}".format(object_list))

    # check lambda object
    obj = _eval_obj(object_list[1], environment)
    if isinstance(obj, lobject.ListData):
        return lobject.Integer(len(obj.list_data))

    if isinstance(obj, lobject.LList):
        return lobject.Integer(len(obj.object_list))

    raise EvalError("Not a ListData or LList. {}".format(obj))


def _eval_range(
    object_list: List[lobject.Object], environment: env.Env
) -> lobject.Object:
    if len(object_list) != 4:
        raise EvalError("Invalid number of arguments for range {}".format(object_list))

    # check lambda object
    start_index = _eval_obj(object_list[1], environment)
    end_index = _eval_obj(object_list[2], environment)
    step_size = _eval_obj(object_list[3], environment)

    if not isinstance(start_index, lobject.Integer):
        raise EvalError("start index must be Integer: {}".format(start_index))
    if not isinstance(end_index, lobject.Integer):
        raise EvalError("start index must be Integer: {}".format(start_index))
    if not isinstance(step_size, lobject.Integer):
        raise EvalError("start index must be Integer: {}".format(start_index))

    list_data = [
        lobject.Integer(i) for i in range(start_index.i, end_index.i, step_size.i)
    ]
    return lobject.ListData(list_data)  # type: ignore


def _eval_list(object_list: List[lobject.Object], environment: env.Env):
    head = object_list[0]
    if isinstance(head, lobject.Symbol):
        if head.s in ["+", "-", "*", "/", "%", "<", ">", "=", "!="]:
            return _eval_binary_op(object_list, environment)
        elif head.s == "define":
            return _eval_define(object_list, environment)
        elif head.s == "lambda":
            return _eval_function_def(object_list)
        elif head.s == "if":
            return _eval_if(object_list, environment)
        elif head.s == "list":
            return _eval_list_data(object_list, environment)
        elif head.s == "map":
            return _eval_map(object_list, environment)
        elif head.s == "filter":
            return _eval_filter(object_list, environment)
        elif head.s == "reduce":
            return _eval_reduce(object_list, environment)
        elif head.s == "length":
            return _eval_length(object_list, environment)
        elif head.s == "range":
            return _eval_range(object_list, environment)
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
    if not isinstance(object_list[0], lobject.BinaryOp):
        raise EvalError("Operator must be Symbol. {}".format(object_list[0]))

    op = object_list[0].op
    left = _eval_obj(object_list[1], environment)
    right = _eval_obj(object_list[2], environment)

    left_i = _as_integer(left)
    right_i = _as_integer(right)

    if left_i is not None and right_i is not None:
        return _eval_binary_op_with_intval(op, left_i.i, right_i.i)

    left_s = _as_string(left)
    right_s = _as_string(right)

    if left_s is not None and right_s is not None:
        return _eval_binary_op_with_stringval(op, left_s.string, right_s.string)

    left_f = _as_float(left)
    right_f = _as_float(right)
    if left_f is not None and right_f is not None:
        return _eval_binary_op_with_floatval(op, left_f.f, right_f.f)

    left_l = _as_list(left)
    left_r = _as_list(right)
    if left_l is not None and left_r is not None:
        return _eval_binary_op_with_listdata(op, left_l.list_data, left_r.list_data)

    raise EvalError(
        "Unsupport binary op. op={}, left={}, right={}".format(op, left, right)
    )


def _as_integer(obj: lobject.Object) -> Optional[lobject.Integer]:
    if isinstance(obj, lobject.Integer):
        return obj
    return None


def _as_float(obj: lobject.Object) -> Optional[lobject.Float]:
    if isinstance(obj, lobject.Float):
        return obj
    return None


def _as_string(obj: lobject.Object) -> Optional[lobject.String]:
    if isinstance(obj, lobject.String):
        return obj
    return None


def _as_list(obj: lobject.Object) -> Optional[lobject.ListData]:
    if isinstance(obj, lobject.ListData):
        return obj
    return None


def _eval_binary_op_with_intval(op: str, lhs: int, rhs: int) -> lobject.Object:
    if op == "+":
        return lobject.Integer(lhs + rhs)
    elif op == "-":
        return lobject.Integer(lhs - rhs)
    elif op == "*":
        return lobject.Integer(lhs * rhs)
    elif op == "/":
        return lobject.Integer(lhs // rhs)
    elif op == "%":
        return lobject.Integer(lhs % rhs)
    elif op == "<":
        return lobject.Bool(lhs < rhs)
    elif op == ">":
        return lobject.Bool(lhs > rhs)
    elif op == "=":
        return lobject.Bool(lhs == rhs)
    elif op == "!=":
        return lobject.Bool(lhs != rhs)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))


def _eval_binary_op_with_stringval(op: str, lhs: str, rhs: str) -> lobject.Object:
    if op == "+":
        return lobject.String(lhs + rhs)
    elif op == "<":
        return lobject.Bool(lhs < rhs)
    elif op == ">":
        return lobject.Bool(lhs > rhs)
    elif op == "=":
        return lobject.Bool(lhs == rhs)
    elif op == "!=":
        return lobject.Bool(lhs != rhs)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))


def _eval_binary_op_with_floatval(op: str, lhs: float, rhs: float) -> lobject.Object:
    if op == "+":
        return lobject.Float(lhs + rhs)
    elif op == "-":
        return lobject.Float(lhs - rhs)
    elif op == "*":
        return lobject.Float(lhs * rhs)
    elif op == "/":
        return lobject.Float(lhs / rhs)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))


def _eval_binary_op_with_listdata(
    op: str, lhs: List[lobject.Object], rhs: List[lobject.Object]
) -> lobject.Object:
    if op == "+":
        return lobject.ListData(lhs + rhs)
    else:
        raise EvalError("Invalid infix operator: {}".format(op))
