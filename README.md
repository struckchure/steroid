# steroid

Steroid is a Python library built on top of FastAPI, designed to provide developers with a framework for building high-performance APIs using a structured architecture inspired by NestJs.

# Installation
```bash
$ pip install steroid
```

# Usage

```python
import pydantic
from fastapi import Header, HTTPException, Request

from steroid import Controller, CreateApp, Get, Middleware, Post, UseMiddlewares


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
        return {"hello": "clutchers, savage, and everything else"}

    @Get("not-a-savage")
    def NotASavage():
        return {"hello": "clutchers, not a savage, and everything else"}


def main():
    app = CreateApp()

    app.addController(GreetController)
    app.addController(CluthController)
    app.start()


if __name__ == "__main__":
    main()
```

# Start server
```bash
$ python example.py
[23/07/2023, 19:19:57] INFO [Controller] GreetController {/greetings}
[23/07/2023, 19:19:57] INFO [Method] Mapped {/greetings/greet/{pk}/{gID}, GET} route
[23/07/2023, 19:19:57] INFO [Method] Mapped {/greetings/no-greet, POST} route
[23/07/2023, 19:19:57] INFO [Controller] CluthController {/clutch}
[23/07/2023, 19:19:58] INFO [Method] Mapped {/clutch/savage, GET} route
[23/07/2023, 19:19:58] INFO [Method] Mapped {/clutch/not-a-savage, GET} route
```
