# Module Imports
import sqlite3
from typing import Union
from pydantic import BaseModel, constr, conint
from passlib.context import CryptContext
from passlib import pwd
from hashlib import sha512
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException, Depends, Cookie
from time import time_ns

# Local Module Imports
from app import init_app
from utils.prod import prod

pw_context = CryptContext(schemes=["bcrypt"])

app = init_app()

con = sqlite3.connect('data.sqlite')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS Users(
    UserID TEXT PRIMARY KEY,
    Password TEXT,
    WeeklyTarget INTEGER
)''')

#Table 2: expenses table
cur.execute('''CREATE TABLE IF NOT EXISTS Expenses(
    UserID TEXT,
    Cost INTEGER,
    Time INTEGER, 
    Category TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)''')

#Table 3: sessions table
cur.execute('''CREATE TABLE IF NOT EXISTS Sessions(
    Token TEXT PRIMARY KEY,
    UserID TEXT,
    Timestamp INTEGER,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)''')

con.commit()
con.close()


@app.get("/")
def read_root():
    return {"magic": "tester boi 101"}

class UserCredentials(BaseModel):
    id: constr(strip_whitespace=True, min_length=3, max_length=20, regex='^[A-Za-z0-9_]+$')
    password: constr(min_length=3, max_length=80)

class User(BaseModel):
    id: str
    hashed_token: str


def generateSessionTokenWithCookieResponse(user: UserCredentials):
    res = JSONResponse({"success": True})
    
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
        secure=prod,
        domain="thrifty.pages.dev" if prod else None
    )

    hashed_token = sha512(token.encode("utf-8")).hexdigest()

    time = time_ns()

    con = sqlite3.connect('data.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO Sessions VALUES (?, ?, ?)", (hashed_token, user.id, time))
    con.commit()
    con.close()
    
    return res


@app.post("/register/")
def register(user: UserCredentials):
    success = False
    salted_pw = pw_context.hash(user.password)
    data = (user.id, salted_pw, 0)
    try:
        con = sqlite3.connect('data.sqlite')
        cur = con.cursor()
        cur.execute("INSERT INTO Users VALUES (?, ?, ?)", data)
        con.commit()
        con.close()
        
        # Set cookie and return
        return generateSessionTokenWithCookieResponse(user)

    except sqlite3.Error as er:
        print(er)
    return {"success": False}

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

@app.post("/login/")
def login(user: UserCredentials):
    try:
        con = sqlite3.connect('data.sqlite')
        cur = con.cursor()
        cur.execute("SELECT Password FROM Users WHERE UserID=? COLLATE NOCASE", (user.id,))
        db_password = cur.fetchone()
        con.close()
        
        if (db_password is not None):
            if (pw_context.verify(user.password, db_password[0])):
                return generateSessionTokenWithCookieResponse(user)
        
    except sqlite3.Error as er:
        print(er)
    raise credentials_exception

def get_user(token: Union[str, None] = Cookie(default=None, alias="session")):
    # Delete all expired tokens
    limit = time_ns() - (14 * 86400 * pow(10, 9))
    con = sqlite3.connect('data.sqlite')
    cur = con.cursor()
    cur.execute("DELETE FROM Sessions WHERE Timestamp<?", (limit,))
    con.commit()
    con.close()
    
    if token is None:
        raise credentials_exception
    
    hashed_token = sha512(token.encode("utf-8")).hexdigest()

    con = sqlite3.connect('data.sqlite')
    cur = con.cursor()
    cur.execute("SELECT UserID FROM Sessions WHERE Token=?", (hashed_token,))
    result = cur.fetchone()
    con.close()

    if (result is None):
        raise credentials_exception

    return User(id=result[0], hashed_token=hashed_token)

@app.get("/is_logged_in/")
def is_logged_in(user: User = Depends(get_user)):
    return True

@app.post("/logout/")
def logout(user: User = Depends(get_user)):
    con = sqlite3.connect('data.sqlite')
    cur = con.cursor()
    cur.execute("DELETE FROM Sessions WHERE Token=?", (user.hashed_token,))
    con.commit()
    con.close()

    res = JSONResponse({"success": True})
    res.delete_cookie("session")
    return res

class UserExpenseEntry(BaseModel):
    cost: conint(gt=0)
    category: str = "Others"
    time: Union[int, None]


# TODO add proper responses here
@app.post("/expenses/create/")
def create_expense(expense: UserExpenseEntry, user: User = Depends(get_user)):
    db_error = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error creating record in database"
    )

    if expense.time is None:
        expense.time = time_ns()

    print(expense)
    try:        
        con = sqlite3.connect('data.sqlite')
        cur = con.cursor()
        cur.execute("INSERT INTO Expenses VALUES (?, ?, ?, ?)", (user.id, expense.cost, expense.time, expense.category))
        con.commit()
        con.close()
    except sqlite3.Error as er:
        print(er)
        raise db_error


# Amazing Akira code:

@app.get("/user_info/{username}")
def user_info(username: str):
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE UserID=?", (username,))
    rows = cur.fetchall()

    for row in rows:
        return{row} 

@app.get("/user_catagory/{username}/{catagory}")
def user_catagoty(username: str, catagory: str):
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE UserID=? and Catagory=?", (username,),(catagory,))
    rows = cur.fetchall()
    for row in rows:
        return{row}
