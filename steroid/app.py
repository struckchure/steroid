import uvicorn
from fastapi import FastAPI

from steroid.common import Controller
from steroid.utils import removeLeadingOrTrailingSlash

app = FastAPI()


class CreateApp:
    _APP: FastAPI = None

    def __new__(cls, *args, **kwargs):
        if cls._APP is None:
            cls._APP = FastAPI(*args, **kwargs)

        return cls

    @classmethod
    @property
    def app(cls):
        return cls._APP

    @classmethod
    def start(cls, *args, **kwargs):
        uvicorn.run(cls.app, *args, **kwargs)

    @classmethod
    def addController(cls, controller: Controller):
        cls.app.include_router(
            controller.router,
            prefix=controller.path,
            tags=[removeLeadingOrTrailingSlash(controller.path)]
            if controller.path
            else [],
        )
