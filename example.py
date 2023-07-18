import pydantic
from typing_extensions import TypedDict

from steroid.app import CreateApp
from steroid.common import Controller, Get, Post


class Salute(pydantic.BaseModel):
    aye: str


class Hello(TypedDict):
    pk: str
    gID: int


class GreetResponse(TypedDict):
    hello: Hello


class NoHello(TypedDict):
    aye: str


class NoGreetResponse(TypedDict):
    noHello: NoHello


@Controller()
class GreetController:
    @Get("greet/{pk}/{gID}")
    def Greet(pk: str, gID: int) -> GreetResponse:
        return {"hello": {"pk": pk, "gID": gID}}

    @Post("no-greet")
    def NoGreet(salute: Salute) -> NoGreetResponse:
        return {"noHello": salute}


app = CreateApp()

app.addController(GreetController)
app.start()
