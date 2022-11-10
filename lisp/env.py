from typing import Mapping, Optional

from lisp import lobject


class Env(object):
    vars: Mapping[str, lobject.Object]

    def __init__(self, parent) -> None:
        self.parent = parent
        self.vars = {}

    def get(self, name: str) -> Optional[lobject.Object]:
        v = self.vars.get(name, None)
        if v is not None:
            return v

        if self.parent is not None:
            return self.parent.get(name)

        return None

    def set(self, name: str, val: lobject.Object):
        self.vars[name] = val


def new() -> Env:
    return Env(None)


def extend(parent: Env) -> Env:
    return Env(parent)
