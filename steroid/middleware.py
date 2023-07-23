import inspect
from typing import Literal, Union

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from steroid.constants import (
    APP_COMPONENT,
    APP_COMPONENT_TYPE,
    APP_METHOD_MIDDLEWARE,
    APP_MIDDLEWARE_TARGET,
)
from steroid.utils import getApp, removeLeadingOrTrailingSlash


class Middleware:
    HOOK: Union[Literal["PRE"], Literal["POST"]] = "PRE"

    def __call__(self, cls):
        return cls

    def action(request: Request):
        raise NotImplementedError("Middleware action must be implemented")


class UseMiddlewares:
    _APPLY_TO_PATH: str = None
    _APPLY_TO_METHOD: str = None

    _PRE_MIDDLEWARES: list[Middleware] = []
    _POST_MIDDLEWARES: list[Middleware] = []

    def __init__(self, *middlewares: list[Middleware]):
        self._PRE_MIDDLEWARES = [
            middleware for middleware in middlewares if middleware.HOOK == "PRE"
        ]
        self._POST_MIDDLEWARES = [
            middleware for middleware in middlewares if middleware.HOOK == "POST"
        ]

    def __call__(self, func):
        if not inspect.isfunction(func):
            raise Exception("Middlewares can only be applied to functions")

        self.func = func

        setattr(self.func, APP_MIDDLEWARE_TARGET, getattr(func, APP_COMPONENT, None))
        setattr(self.func, APP_COMPONENT_TYPE, APP_METHOD_MIDDLEWARE)
        setattr(self.func, APP_COMPONENT, self)

        return self.func

    def setupMiddleware(self):
        method = getattr(self.func, APP_MIDDLEWARE_TARGET, None)

        if method:
            self._APPLY_TO_PATH = f"{removeLeadingOrTrailingSlash(method._CONTROLLER.path)}/{removeLeadingOrTrailingSlash(method._PATH)}"
            self._APPLY_TO_METHOD = method._METHOD

        async def _handleMiddlewareRoutes(request: Request, call_next):
            try:
                self.handleMiddlewares(request, self._PRE_MIDDLEWARES)

                response = await call_next(request)

                self.handleMiddlewares(request, self._POST_MIDDLEWARES)

                return response
            except HTTPException as error:
                return JSONResponse(
                    status_code=error.status_code, content={"detail": error.detail}
                )

        getApp().middleware("http")(_handleMiddlewareRoutes)

        return self.func

    def handleMiddlewares(self, request: Request, middlewares: list[Middleware]):
        path = removeLeadingOrTrailingSlash(request.url.path)
        method = request.method

        if method == self._APPLY_TO_METHOD and path == self._APPLY_TO_PATH:
            for middleware in middlewares:
                middleware.action(request)
