from fastapi import FastAPI

import db.core as db
from routes import auth, expenses, settings

db.init()

app = FastAPI(root_path="/api")

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(settings.router)

@app.get("/")
def read_root():
    return ["Thrifty API.", "Visit /docs for API Documentation."]
