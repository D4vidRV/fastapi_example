from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    name: str
    email: str

class UserPost(BaseModel):
    name: str
    email: str
    password: str
