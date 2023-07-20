# steroid

Steroid is a Python library built on top of FastAPI, designed to provide developers with a framework for building high-performance APIs using a structured architecture inspired by NestJs.

# Installation
```bash
$ pip install steroid
```

# Usage

```python
from typing import Union

import pydantic
from fastapi import Header, HTTPException, Request
from typing_extensions import TypedDict

from steroid import Controller, CreateApp, Get, Middleware, Post, UseMiddlewares


class Salute(pydantic.BaseModel):
  aye: str


class Hello(TypedDict):
  pk: str
  gID: int
  XToken: Union[str, None]


class GreetResponse(TypedDict):
  hello: Hello


class NoHello(TypedDict):
  aye: str


class NoGreetResponse(TypedDict):
  noHello: NoHello


class AuthMiddleware(Middleware):
  HOOK = "PRE"

  def action(request: Request):
    authToken = request.headers.get("Authorization")
    if not authToken:
      raise HTTPException(status_code=401, detail="Unauthorized")


class PreMiddleware(Middleware):
  HOOK = "PRE"

  def action(request: Request):
    print("hello")


class PostMiddleware(Middleware):
  HOOK = "POST"

  def action(request: Request):
    print("bye")


@UseMiddlewares(AuthMiddleware)
@Controller("greetings")
class GreetController:
  @Get("greet/{pk}/{gID}")
  def Greet(
    pk: str,
    gID: int,
    x_token: str = Header(default=None),
  ) -> GreetResponse:
    return {"hello": {"pk": pk, "gID": gID, "XToken": x_token}}

  @Post("no-greet")
  def NoGreet(salute: Salute) -> NoGreetResponse:
      return {"noHello": salute}


@UseMiddlewares(PreMiddleware, PostMiddleware)
@Controller("clutch")
class CluthController:
  @Get("savage")
  def Savage():
      return {"hello": "clutchers, savage, and everything else"}


app = CreateApp()

app.addController(GreetController)
app.addController(CluthController)

if __name__ == "__main__":
  app.start()

```