import inspect

from steroid.constants import APP_COMPONENT, APP_COMPONENT_TYPE, APP_CONTROLLER_METHOD
from steroid.utils import formatPath, removeLeadingOrTrailingSlash


class BaseMethod:
    _METHOD: str = None
    _PATH: str = None
    _FULL_PATH: str = None

    _CONTROLLER = None

    def __init__(self, path: str = "", *args, **kwargs):
        self._PATH = formatPath(path)

        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        self.func = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(wrapper, APP_COMPONENT_TYPE, APP_CONTROLLER_METHOD)
        setattr(wrapper, APP_COMPONENT, self)

        return wrapper

    def setupMethod(self, controller):
        self._CONTROLLER = controller

        httpMethodDecorator = getattr(controller.router, self._METHOD.lower())
        parameters = [
            parameter
            for parameter in dict(inspect.signature(self.func).parameters).values()
        ]
        httpMethodDecorator(self.path)(self.func)(*parameters)

    @property
    def path(self):
        return f"/{removeLeadingOrTrailingSlash(self._PATH)}/"


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
