from typing import Union
from pydantic import BaseModel, constr, condecimal

class UserCredentials(BaseModel):
    """User data transmitted from client to server"""

    id: constr(strip_whitespace=True, min_length=3, max_length=20, regex='^[A-Za-z0-9_]+$')
    password: constr(min_length=3, max_length=80)


class User(BaseModel):
    """User data stored in database"""

    id: str
    hashed_token: str


class UserExpenseEntry(BaseModel):
    cost: condecimal(gt=0, decimal_places=2)
    category: str = "others"
    title: str
    timestamp: Union[int, None]
    description: Union[str, None]
