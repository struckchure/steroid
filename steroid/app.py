import os
from typing import Union

import uvicorn
from fastapi import FastAPI

from steroid.constants import APP_COMPONENT, APP_COMPONENT_TYPE, APP_CONTROLLER
from steroid.controller import Controller
from steroid.logging import getLogConfig, getLogger
from steroid.utils import clearTerminal


class CreateApp:
    _APP: FastAPI = None
    logger = None

    def __new__(cls, *args, **kwargs):
        if cls._APP is None:
            cls.logger = getLogger()
            cls._APP = FastAPI(*args, **kwargs)

        return cls

    @classmethod
    @property
    def app(cls):
        return cls._APP

    @classmethod
    def start(cls, host: str = "0.0.0.0", port: int = 8000):
        clearTerminal()

        uvicorn.run(cls.app, host=host, port=port, log_config=getLogConfig())

    @classmethod
    def addController(cls, controller):
        componentType = getattr(controller, APP_COMPONENT_TYPE, None)
        component: Union[Controller, None] = getattr(controller, APP_COMPONENT, None)

        if not componentType == APP_CONTROLLER:
            raise Exception(f"Controller component must be of type {APP_CONTROLLER}")

        if not component:
            raise Exception(f"Controller component not detected")

        component.setupController(cls.app)
