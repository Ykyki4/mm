from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""


class LoginUser(BaseModel):
    username: str
    password: str
