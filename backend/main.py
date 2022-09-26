from fastapi import FastAPI

import db.core as db
from routes import auth, expenses

db.init()

app = FastAPI(root_path="/api")

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/")
def read_root():
    return {"magic": "tester boi 101"}


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
