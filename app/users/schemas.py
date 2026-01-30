from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""


class LoginUser(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str = ""
    last_name: str = ""
