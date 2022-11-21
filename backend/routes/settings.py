import sqlite3
from decimal import Decimal
from pydantic import condecimal
from fastapi import Depends, APIRouter

import db.core as db
from db.models import User
from routes.dependencies import get_user
from utils.exceptions import db_read_exception, db_write_exception

router = APIRouter(
    prefix="/settings",
    tags=["user_settings"]
)

@router.patch("/weekly_target/{amount}")
def set_weekly_target(amount: condecimal(ge=0, decimal_places=2), user: User = Depends(get_user)):
    try:
        con, cur = db.get_both()
        cur.execute(
            "UPDATE Users SET WeeklyTarget=? WHERE UserID=? COLLATE NOCASE",
            (int(amount * 100), user.id,)
        )
        db.safe_close(con)
        return True
    except sqlite3.Error as er:
        print(er)
        raise db_write_exception

@router.get("/weekly_target/")
def get_weekly_target(user: User = Depends(get_user)):
    try:
        con, cur = db.get_both()
        cur.execute(
            "SELECT WeeklyTarget FROM Users WHERE UserID=? COLLATE NOCASE",
            (user.id,)
        )
        target = Decimal(cur.fetchone()[0])/100
        con.close()
        return target
    except sqlite3.Error as er:
        print(er)
        raise db_read_exception
