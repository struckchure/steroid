import inspect
from typing import Any

from fastapi.routing import APIRouter

from steroids.utils import formatPath


class Controller:
    def __init__(self, path: str = "", *args, **kwargs):
        self.router = APIRouter()

        self.path = formatPath(path)

        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls):
        setattr(cls, "path", self.path)
        setattr(cls, "router", self.router)

        for name, method in cls.__dict__.items():
            methodClass = getattr(method, "object", None)
            if isinstance(methodClass, Method):
                methodClass.register(self.router)

        return cls(*self.args, **self.kwargs)


class Method:
    _METHOD: str

    def __init__(self, path: str = "", *args, **kwargs):
        self.path = formatPath(path)

        self.args = args
        self.kwargs = kwargs

        self.route = None

    def register(self, router):
        self.__call__(self.func, router)

    def __call__(self, func, router=None):
        # TODO: alot feels very wrong in this method, help me!

        self.func = func

        if router:
            httpMethodDecorator = getattr(router, self._METHOD.lower())

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            parameters = [
                parameter
                for parameter in dict(inspect.signature(func).parameters).values()
            ]

            httpMethodDecorator(self.path)(func)(*parameters)

            return wrapper

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(wrapper, "object", self)

        return wrapper


class Get(Method):
    _METHOD = "GET"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Post(Method):
    _METHOD = "POST"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
