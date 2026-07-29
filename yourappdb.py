import sqlite3
from flask import g

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    mydb = get_db()
    cur = mydb.execute(query, args)
    if "insert into" in query:
        mydb.commit()

    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
