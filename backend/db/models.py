from typing import Union
from pydantic import BaseModel, constr, conint

class UserCredentials(BaseModel):
    """User data transmitted from client to server"""

    id: constr(strip_whitespace=True, min_length=3, max_length=20, regex='^[A-Za-z0-9_]+$')
    password: constr(min_length=3, max_length=80)


class User(BaseModel):
    """User data stored in database"""

    id: str
    hashed_token: str


class UserExpenseEntry(BaseModel):
    cost: conint(gt=0)
    category: str = "Others"
    time: Union[int, None]
