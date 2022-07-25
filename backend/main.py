from typing import Union
import os

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
