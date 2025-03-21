from pydantic import BaseModel


class User(BaseModel):
    username: str | None = None
    password: str | None = None
