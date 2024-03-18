from typing import Union

import pydantic


class LoginDto(pydantic.BaseModel):
    username: str
    password: str


class RegisterDto(pydantic.BaseModel):
    first_name: Union[str, None] = pydantic.Field(default=None)
    last_name: Union[str, None] = pydantic.Field(default=None)
    username: str
    password: str


class UpdateDto(pydantic.BaseModel):
    first_name: Union[str, None] = pydantic.Field(default=None)
    last_name: Union[str, None] = pydantic.Field(default=None)
    username: Union[str, None] = pydantic.Field(default=None)
    password: Union[str, None] = pydantic.Field(default=None)
