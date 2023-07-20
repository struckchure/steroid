import inspect

from steroid.utils import formatPath


class BaseMethod:
    _METHOD: str

    def __init__(self, path: str = "", *args, **kwargs):
        self.path = formatPath(path)

        self.args = args
        self.kwargs = kwargs

        self.route = None

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

    def mapSelfToRouter(self, router):
        self.__call__(self.func, router)


class Get(BaseMethod):
    _METHOD = "GET"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Post(BaseMethod):
    _METHOD = "POST"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Put(BaseMethod):
    _METHOD = "PUT"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Patch(BaseMethod):
    _METHOD = "PATCH"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Delete(BaseMethod):
    _METHOD = "DELETE"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
