import sqlite3
from passlib.context import CryptContext
from passlib import pwd
from hashlib import sha512
from fastapi.responses import JSONResponse
from fastapi import Depends, APIRouter

from utils.prod import prod
from utils.time import time_ms
from utils.exceptions import credentials_exception
from routes.dependencies import get_user
from db import core as db
from db.models import User, UserCredentials

router = APIRouter()
pw_context = CryptContext(schemes=["bcrypt"])

def generateSessionTokenWithCookieResponse(user: UserCredentials):
    res = JSONResponse(True)
    
    token = pwd.genword(256)
    res.set_cookie(
        key="session",
        value=token,

        # Restrict cookie access from JavaScript
        httponly=True,

        # 14 days max age for cookie
        max_age=14*86400,

        # Set samesite to none only in the HTTPS-enabled production environment
        samesite="none" if prod else "lax",
        secure=prod
    )

    hashed_token = sha512(token.encode("utf-8")).hexdigest()

    time = time_ms()

    con, cur = db.get_both()
    cur.execute("INSERT INTO Sessions VALUES (?, ?, ?)", (hashed_token, user.id, time))
    db.safe_close(con)
    
    return res


@router.post("/register/")
def register(user: UserCredentials):
    salted_pw = pw_context.hash(user.password)
    data = (user.id, salted_pw, 0)
    try:
        con, cur = db.get_both()
        cur.execute("INSERT INTO Users VALUES (?, ?, ?)", data)
        db.safe_close(con)
        
        # Set cookie and return
        return generateSessionTokenWithCookieResponse(user)

    except sqlite3.Error as er:
        print(er)
    return False


@router.post("/login/")
def login(user: UserCredentials):
    try:
        con, cur = db.get_both()
        cur.execute("SELECT Password FROM Users WHERE UserID=? COLLATE NOCASE", (user.id,))
        db_password = cur.fetchone()
        con.close()
        
        if (db_password is not None):
            if (pw_context.verify(user.password, db_password[0])):
                return generateSessionTokenWithCookieResponse(user)
        
    except sqlite3.Error as er:
        print(er)
    raise credentials_exception


@router.get("/is_logged_in/")
def is_logged_in(user: User = Depends(get_user)):
    return True


@router.post("/logout/")
def logout(user: User = Depends(get_user)):
    con, cur = db.get_both()
    cur.execute("DELETE FROM Sessions WHERE Token=?", (user.hashed_token,))
    db.safe_close(con)    

    res = JSONResponse(True)
    res.delete_cookie(
        key="session",
        
        # Set samesite to none only in the HTTPS-enabled production environment
        samesite="none" if prod else "lax",
        secure=prod
    )
    return res
