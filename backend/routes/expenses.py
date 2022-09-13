import sqlite3
from fastapi import Depends, APIRouter

import db.core as db
from db.models import UserExpenseEntry, User
from routes.dependencies import get_user
from utils.exceptions import db_exception
from utils.time import time_ms

router = APIRouter()

# TODO add proper responses here
@router.post("/expenses/create/")
def create_expense(expense: UserExpenseEntry, user: User = Depends(get_user)):

    if expense.timestamp is None:
        expense.timestamp = time_ms()

    try:
        con, cur = db.get_both()
        cur.execute(
            "INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?)",
            (user.id, expense.title, int(expense.cost * 100), expense.timestamp, expense.category, expense.description)
        )
        db.safe_close(con)
        return True
    except sqlite3.Error as er:
        print(er)
        raise db_exception
