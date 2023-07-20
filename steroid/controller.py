from typing import Any

from fastapi.routing import APIRouter

from steroid.methods import BaseMethod
from steroid.utils import formatPath


class Controller:
    def __init__(self, path: str = "", *args, **kwargs):
        self.router = APIRouter()

        self.path = formatPath(path)

        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls):
        self.setupController(cls)

        methods = list(self.findMethods(cls))
        self.mapMethodsToController(methods)

        return cls(*self.args, **self.kwargs)

    def setupController(self, classObject):
        setattr(classObject, "path", self.path)
        setattr(classObject, "router", self.router)

    def findMethods(self, classObject):
        for _, method in classObject.__dict__.items():
            methodClass = getattr(method, "object", None)
            if isinstance(methodClass, BaseMethod):
                yield methodClass

    def mapMethodsToController(self, methods: list[BaseMethod]):
        return list(
            map(lambda method: method.mapSelfToRouter(router=self.router), methods)
        )
