import os

import uvicorn
from fastapi import FastAPI
from watchfiles import Change, DefaultFilter, run_process

from steroid.controller import Controller
from steroid.logging import getLogger
from steroid.utils import clearTerminal, removeLeadingOrTrailingSlash


class OnlyPythonFilesFilter(DefaultFilter):
    allowed_extensions = ".py"

    def __call__(self, change: Change, path: str) -> bool:
        return super().__call__(change, path) and path.endswith(self.allowed_extensions)


class CreateApp:
    _APP: FastAPI = None
    logger = getLogger()

    def __new__(cls, *args, **kwargs):
        if cls._APP is None:
            cls._APP = FastAPI(*args, **kwargs)

        return cls

    @classmethod
    @property
    def app(cls):
        return cls._APP

    @classmethod
    def _start(cls):
        clearTerminal()

        uvicorn.run(cls.app)

    @classmethod
    def onFileChange(cls, change: Change):
        getLogger().info(f"reloading ... file changes in {change}")

    @classmethod
    def start(cls, reload=True):
        if reload == False:
            cls._start()
            return

        watchFilePath = os.getcwd()

        run_process(
            watchFilePath,
            target=cls._start,
            callback=cls.onFileChange,
            watch_filter=OnlyPythonFilesFilter(),
        )

    @classmethod
    def addController(cls, controller: Controller):
        cls.app.include_router(
            controller.router,
            prefix=controller.path,
            tags=[removeLeadingOrTrailingSlash(controller.path)]
            if controller.path
            else [],
        )
        cls.logger.info(f"Mapped {controller.path} to router")
