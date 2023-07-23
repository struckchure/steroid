import inspect

from fastapi.routing import APIRouter

from steroid.constants import (
    APP_COMPONENT,
    APP_COMPONENT_TYPE,
    APP_CONTROLLER,
    APP_CONTROLLER_METHOD,
    APP_METHOD_MIDDLEWARE,
    APP_MIDDLEWARE_TARGET,
)
from steroid.logging import getLogger
from steroid.utils import formatPath, removeLeadingOrTrailingSlash

logger = getLogger()


class Controller:
    def __init__(self, path: str = "", *args, **kwargs):
        self.router = APIRouter()

        self.path = formatPath(path)

        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls):
        self.cls = cls

        self.mapComponentsToController(cls)

        setattr(cls, APP_COMPONENT_TYPE, APP_CONTROLLER)
        setattr(cls, APP_COMPONENT, self)

        return cls(*self.args, **self.kwargs)

    def setupController(self, app):
        app.include_router(
            self.router,
            prefix=self.path,
            tags=[removeLeadingOrTrailingSlash(self.path)] if self.path else [],
        )

    def mapComponentsToController(self, classObject):
        logger.info("[Controller] %s {%s}" % (self.cls.__name__, self.path))

        for _, method in classObject.__dict__.items():
            if inspect.isfunction(method):
                componentType = getattr(method, APP_COMPONENT_TYPE, None)
                component = getattr(method, APP_COMPONENT, None)
                if componentType == APP_CONTROLLER_METHOD:
                    self.handleAppControllerMethod(component)
                elif componentType == APP_METHOD_MIDDLEWARE:
                    self.handleAppMethodMiddleware(component)

    def handleAppControllerMethod(self, component):
        setupControllerMethod = getattr(component, "setupMethod", None)
        if setupControllerMethod:
            setupControllerMethod(self)

            logger.info(
                "[Method] Mapped {%s%s, %s} route"
                % (self.path, component._PATH, component._METHOD)
            )

    def handleAppMethodMiddleware(self, component):
        middlewareTarget = getattr(component.func, APP_MIDDLEWARE_TARGET, None)
        self.handleAppControllerMethod(middlewareTarget)

        setupMiddleware = getattr(component, "setupMiddleware", None)
        if setupMiddleware:
            setupMiddleware()
