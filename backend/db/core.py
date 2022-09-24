import sqlite3

FILENAME = "data.sqlite"

def get_con():
    return sqlite3.connect(FILENAME)

def get_both():
    con = get_con()
    return con, con.cursor()

def safe_close(connector: sqlite3.Connection):
    connector.commit()
    connector.close()

def init():
    con, cur = get_both()

    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS Users(
        UserID TEXT PRIMARY KEY COLLATE NOCASE,
        Password TEXT,
        WeeklyTarget INTEGER
    )''')

    # Table 2: expenses table
    cur.execute('''CREATE TABLE IF NOT EXISTS Expenses(
        UserID TEXT COLLATE NOCASE,
        Title TEXT,
        Cost INTEGER,
        Time INTEGER,
        Category TEXT,
        Description TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )''')

    # Table 3: sessions table
    cur.execute('''CREATE TABLE IF NOT EXISTS Sessions(
        Token TEXT PRIMARY KEY,
        UserID TEXT COLLATE NOCASE,
        Timestamp INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )''')

    safe_close(con)
