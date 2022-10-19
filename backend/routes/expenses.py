import sqlite3
from decimal import Decimal
from typing import Union
from fastapi import Depends, APIRouter, Query

import db.core as db
from db.models import UserExpenseEntry, User
from routes.dependencies import get_user
from utils.exceptions import db_read_exception, db_write_exception
from utils.time import time_ms

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)

@router.post("/create/")
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
        raise db_write_exception


def get_expenses_data(user_id, category, timestamp_start, timestamp_end, columns = "*", num_rows = None):
    query = "SELECT %s FROM Expenses WHERE UserID=?" % columns
    values = (user_id,)

    if category:
        query += " AND Category IN (%s)" % ",".join("?" * len(category))
        values += tuple(category)
    
    if timestamp_start:
        query += " AND Time>=?"
        values += (timestamp_start,)

    if timestamp_end:
        query += " AND Time<?"
        values += (timestamp_end,)

    query += " ORDER BY Time DESC"

    try:
        con, cur = db.get_both()
        cur.execute(query, values)
        sql_res = cur.fetchmany(num_rows) if num_rows else cur.fetchall()
        con.close()
        return sql_res
    except sqlite3.Error as er:
        print(er)
        raise db_read_exception


@router.get("/total/")
def get_expenses_total(
    category: Union[None, list[str]] = Query(default=None),
    timestamp_start: Union[None, int] = None,
    timestamp_end: Union[None, int] = None,
    user: User = Depends(get_user)
):
    sql_res = get_expenses_data(user.id, category, timestamp_start, timestamp_end, "SUM(Cost)", 1)[0][0]
    sql_res = sql_res or 0
    return Decimal(sql_res)/100


@router.get("/")
def get_expenses(
    category: Union[None, list[str]] = Query(default=None),
    timestamp_start: Union[None, int] = None,
    timestamp_end: Union[None, int] = None,
    count: Union[None, int] = None,
    user: User = Depends(get_user)
):
    sql_res = get_expenses_data(user.id, category, timestamp_start, timestamp_end, "*, rowid", count)
    res = []
    for entry in sql_res:
        res.append({
            "id": entry[6],
            "category": entry[4],
            "title": entry[1],
            "timestamp": entry[3],
            "cost": Decimal(entry[2])/100,
            "description": entry[5]
        })
    return res


@router.delete("/delete/{expense_id}")
def delete_expense(expense_id: int, user: User = Depends(get_user)):
    try:
        con, cur = db.get_both()
        cur.execute(
            "DELETE FROM Expenses WHERE UserID=? AND rowid=?",
            (user.id, expense_id)
        )
        db.safe_close(con)
        return True
    except sqlite3.Error as er:
        print(er)
        raise db_write_exception


@router.put("/edit/{expense_id}")
def edit_expense(expense: UserExpenseEntry, expense_id: int, user: User = Depends(get_user)):
    if expense.timestamp is None:
        expense.timestamp = time_ms()

    try:
        con, cur = db.get_both()
        cur.execute(
            "UPDATE Expenses SET Title=?, Cost=?, Time=?, Category=?, Description=? WHERE UserID=? AND rowid=?",
            (expense.title, int(expense.cost * 100), expense.timestamp, expense.category, expense.description, user.id, expense_id)
        )
        db.safe_close(con)
        return True
    except sqlite3.Error as er:
        print(er)
        raise db_write_exception
