from typing import Union
from fastapi import Cookie
from hashlib import sha512

import db.core as db
from db.models import User
from utils.time import time_ms
from utils.exceptions import credentials_exception

def get_user(token: Union[str, None] = Cookie(default=None, alias="session")):
    # Delete all expired tokens (Expired = 14 days old or more)
    limit = time_ms() - (14 * 86400 * pow(10, 3))
    
    con, cur = db.get_both()
    cur.execute("DELETE FROM Sessions WHERE Timestamp<?", (limit,))
    db.safe_close(con)

    if token is None:
        raise credentials_exception
    
    hashed_token = sha512(token.encode("utf-8")).hexdigest()

    con, cur = db.get_both()
    cur.execute("SELECT UserID FROM Sessions WHERE Token=?", (hashed_token,))
    result = cur.fetchone()
    con.close()

    if (result is None):
        raise credentials_exception

    return User(id=result[0], hashed_token=hashed_token)
