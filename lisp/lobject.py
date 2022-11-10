from abc import ABC
from enum import IntEnum, auto
from typing import List


class ObjectType(IntEnum):
    VOID = auto()
    INTEGER = auto()
    BOOL = auto()
    SYMBOL = auto()
    LAMBDA = auto()
    LIST = auto()


class Object(ABC):
    object_type: ObjectType

    def __init__(self, object_type: ObjectType):
        self.object_type = object_type

    def __eq__(self, other: object) -> bool:
        if other is None or type(self) != type(other):
            return False

        return self.object_type == other.object_type

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class _Void(Object):
    def __init__(self):
        super().__init__(ObjectType.VOID)

    def __str__(self) -> str:
        return "Void"


Void = _Void()


class Integer(Object):
    def __init__(self, i: int):
        super().__init__(ObjectType.INTEGER)
        self.i = i

    def __str__(self) -> str:
        return "{}".format(self.i)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.i == other.i


class Symbol(Object):
    def __init__(self, s: str):
        super().__init__(ObjectType.SYMBOL)
        self.s = s

    def __str__(self) -> str:
        return "{}".format(self.s)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.s == other.s


class Bool(Object):
    def __init__(self, b: bool):
        super().__init__(ObjectType.BOOL)
        self.b = b

    def __str__(self) -> str:
        return "{}".format(self.b)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.b == other.b


class LList(Object):
    def __init__(self, object_list: List[Object]):
        super().__init__(ObjectType.LIST)
        self.l = object_list

    def __eq__(self, other: object) -> bool:
        if not super().__eq__(other):
            return False
        if len(self.l) != len(other.l):
            return False
        for i, e in enumerate(self.l):
            if e != other.l[i]:
                return False
        return True

    def __str__(self) -> str:
        sb = []
        sb.append("(")

        for i, o in enumerate(self.l):
            if i > 0:
                sb.append(" ")
            sb.append("{}".format(o))
        sb.append(")")

        return "".join(sb)


class Lambda(Object):
    def __init__(self, params, body):
        super().__init__(ObjectType.LAMBDA)
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
