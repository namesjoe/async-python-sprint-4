from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str


class PostResponse(BaseModel):
    message: str
