import random

import pydantic
from fastapi import Header, HTTPException, Request

from steroid import App, Controller, Get, Middleware, Post, UseMiddlewares


class Salute(pydantic.BaseModel):
    aye: str


class AuthMiddleware(Middleware):
    HOOK = "POST"

    def action(request: Request):
        authToken = request.headers.get("Authorization")
        if authToken is None or not authToken:
            raise HTTPException(status_code=401, detail="Unauthorized")


class PreMiddleware(Middleware):
    HOOK = "PRE"

    def action(request: Request):
        print("hello")


class PostMiddleware(Middleware):
    HOOK = "POST"

    def action(request: Request):
        print("bye")


@Controller("greetings")
class GreetController:
    @Get("greet/{pk}/{gID}")
    def Greet(
        pk: str,
        gID: int,
        authorization: str = Header(alias="Authorization", default=None),
    ):
        return {"hello": {"pk": pk, "gID": gID, "XToken": authorization}}

    @UseMiddlewares(AuthMiddleware)
    @Post("no-greet")
    def NoGreet(salute: Salute):
        return {"noHello": salute}


@Controller("clutch")
class CluthController:
    @UseMiddlewares(PreMiddleware, PostMiddleware)
    @Get("savage")
    def Savage():
        if (random.randint(0, 10) % 2) == 0:
            raise HTTPException(404, "not found")
        return {"hello": "clutchers, savage, and everything else"}

    @Get("not-a-savage")
    def NotASavage():
        return {"hello": "clutchers, not a savage, and everything else"}


def main():
    app = App()

    app.addController(GreetController)
    app.addController(CluthController)
    app.start()


if __name__ == "__main__":
    main()
