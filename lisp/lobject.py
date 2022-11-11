from abc import ABC
from typing import List


class Object(ABC):
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class _Void(Object):
    def __init__(self):
        super().__init__()

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, _Void):
            return False
        return True

    def __str__(self) -> str:
        return "Void"


Void = _Void()


class Integer(Object):
    def __init__(self, i: int):
        super().__init__()
        self.i = i

    def __str__(self) -> str:
        return "{}".format(self.i)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Integer):
            return False
        return self.i == other.i


class Float(Object):
    def __init__(self, f: float):
        super().__init__()
        self.f = f

    def __str__(self) -> str:
        return "{}".format(self.f)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Float):
            return False
        return self.f == other.f


class Symbol(Object):
    def __init__(self, s: str):
        super().__init__()
        self.s = s

    def __str__(self) -> str:
        return "{}".format(self.s)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Symbol):
            return False
        return self.s == other.s


class String(Object):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def __str__(self) -> str:
        return "{}".format(self.string)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, String):
            return False
        return self.string == other.string


class Bool(Object):
    def __init__(self, b: bool):
        super().__init__()
        self.b = b

    def __str__(self) -> str:
        return "{}".format(self.b)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Bool):
            return False
        return self.b == other.b


class LList(Object):
    def __init__(self, object_list: List[Object]):
        super().__init__()
        self.object_list = object_list

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, LList):
            return False
        return _eq_obj_list(self.object_list, other.object_list)

    def __str__(self) -> str:
        return _obj_list_as_str(self.object_list)


class ListData(Object):
    def __init__(self, list_data: List[Object]):
        super().__init__()
        self.list_data = list_data

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, ListData):
            return False
        return _eq_obj_list(self.list_data, other.list_data)

    def __str__(self) -> str:
        return _obj_list_as_str(self.list_data)


class Lambda(Object):
    def __init__(self, params, body):
        super().__init__()
        self.params: List[str] = params
        self.body: List[Object] = body


# class Lambda(Object):
#     def __init__(self, params: List[str], body: List[Object]):
#         super().__init__(ObjectType.LAMBDA)
#         self.params = params
#         self.body = body

#     def __str__(self) -> str:
#         sb = []
#         sb.append("Lambda(")
#         for param in self.params:
#             sb.append("{} ".format(param))
#         sb.append(")")
#         for expr in self.body:
#             sb.append(" {}".format(expr))
#         return "".join(sb)


def _eq_obj_list(lhs: List[Object], rhs: List[Object]) -> bool:
    if len(lhs) != len(rhs):
        return False
    for i, e in enumerate(lhs):
        if e != rhs[i]:
            return False
    return True


def _obj_list_as_str(obj_list: List[Object]) -> str:
    sb = []
    sb.append("(")

    for i, o in enumerate(obj_list):
        if i > 0:
            sb.append(" ")
        sb.append("{}".format(o))
    sb.append(")")

    return "".join(sb)
