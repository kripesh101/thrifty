from typing import Union
import os
import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

prod = os.getenv("PROD")

origins = ["http://*"]
regex = "http://.*"

if (prod != None):
    origins = [
        "https://thrifty.pages.dev",
        "https://*.thrifty.pages.dev"
    ]
    regex = "https://.*\.thrifty\.pages\.dev"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_origin_regex=regex,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

@app.get("/")
def read_root():
    return {"magic": "tester boi 101"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/register/{username}/{password}")
def register(username: str, password: str):
    success = False
    data = (username, password, 0)
    try:
        con = sqlite3.connect('data.sqlite')
        cur = con.cursor()
        cur.execute("INSERT INTO Users VALUES (?, ?, ?)", data)
        con.commit()
        con.close()
        success = True
    except sqlite3.Error as er:
        print(er)
    return {"success": success}


@app.get("/user_info/{username}")
def user_info(username: str):
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE username=?", (username,))
    rows = cur.fetchall()

    for row in rows:
        return{row} 