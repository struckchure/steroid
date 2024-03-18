from re import U
from typing import TypedDict


class IUser(TypedDict):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    token: str


user_data: list[IUser] = []


class UserModel:
    def list(self):
        return user_data

    def create(self, dto: IUser):
        user_data.append(dto)

        return dto

    def get(self, id: int):
        user = list(filter(lambda x: x.id == id, user_data))
        if len(user) == 0:
            return None

        return user[0]

    def get_by(self, field: str, value: str) -> IUser:
        user = list(filter(lambda x: x[field] == value, user_data))
        if len(user) == 0:
            return None

        return user[0]

    def update(self, id: int, dto: IUser):
        for index, user in enumerate(user_data):
            if user["id"] == id:
                user_data[index] = {**user_data[index], **dto}

                return user_data[index]

        return None

    def delete(self, id: int):
        for index, user in enumerate(user_data):
            if user["id"] == id:
                del user_data[index]

                return True

        return None
