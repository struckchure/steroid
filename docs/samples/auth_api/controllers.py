import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from steroid import Controller, Get, Patch, Post

from dto import LoginDto, RegisterDto, UpdateDto
from guards import AuthGuard
from models import UserModel

user_model = UserModel()


@Controller("user")
class UserController:
    @Get()
    def get(token: Annotated[str, Depends(AuthGuard())]):
        user = user_model.get_by("token", token)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        user.pop("password", None)

        return user

    @Patch()
    def update(token: Annotated[str, Depends(AuthGuard())], dto: UpdateDto):
        user = user_model.get_by("token", token)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        update_user = user_model.update(user["id"], dto)
        update_user.pop("password", None)

        return update_user


@Controller("auth")
class AuthController:
    @Post("login")
    def login(dto: LoginDto):
        user = user_model.get_by("username", dto.username)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

        if user["password"] != dto.password:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid credentials")

        user.pop("password", None)

        return user

    @Post("register")
    def register(dto: RegisterDto):
        user = user_model.get_by("username", dto.username)
        if user is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "user already exists")

        created_user = user_model.create(
            {
                "username": dto.username,
                "password": dto.password,
                "first_name": dto.first_name,
                "last_name": dto.last_name,
                "token": secrets.token_hex(6),
            }
        )
        created_user.pop("password", None)

        return created_user
