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

import sqlite3
con = sqlite3.connect('data.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE stocks
               (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

@app.get("/")
def read_root():
    return {"Salong": "Gay boi 101"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
