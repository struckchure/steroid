import os
from subprocess import call


def formatPath(text: str) -> str:
    if len(text) == 0:
        return text
    return f"/{text}" if not text.startswith("/") else text


def removeLeadingOrTrailingSlash(text: str) -> str:
    if text.startswith("/"):
        text = text[1:]
    if text.endswith("/"):
        text = text[:-1]

    return text


def getApp():
    from steroid.app import CreateApp

    return CreateApp().app


def clearTerminal():
    print("\033c", end="")
