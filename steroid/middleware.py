from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from steroid.utils import getApp


class Middleware:
    HOOK: str = "PRE"

    def __call__(self, cls):
        return cls

    def action(request: Request):
        raise NotImplementedError("Middleware action must be implemented")


class UseMiddlewares:
    _PRE_MIDDLEWARES: list[Middleware] = []
    _POST_MIDDLEWARES: list[Middleware] = []

    def __init__(self, *middlewares: list[Middleware]):
        pre_middlewares = []
        post_middlewares = []

        for middleware in middlewares:
            if middleware.HOOK == "PRE":
                pre_middlewares.append(middleware)
            elif middleware.HOOK == "POST":
                post_middlewares.append(middleware)

        self._PRE_MIDDLEWARES = pre_middlewares
        self._POST_MIDDLEWARES = post_middlewares

    def __call__(self, cls):
        applyMiddlewareToRoute = getattr(cls, "path")

        async def routeMiddlewareAction(request: Request, call_next):
            try:
                canApplyToRoute = request.url.path.startswith(applyMiddlewareToRoute)

                if canApplyToRoute:
                    for middleware in self._PRE_MIDDLEWARES:
                        middleware.action(request)

                response = await call_next(request)

                if canApplyToRoute:
                    for middleware in self._POST_MIDDLEWARES:
                        middleware.action(request)

                return response
            except HTTPException as error:
                return JSONResponse(
                    status_code=error.status_code, content={"detail": error.detail}
                )

        rootApp = getApp()
        rootApp.middleware("http")(routeMiddlewareAction)

        return cls
