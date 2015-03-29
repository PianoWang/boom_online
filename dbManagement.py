from sqlite3 import dbapi2 as sqlite3
from flask import g
from flaskTest import app
import hashlib


def connect_db():
    """Connects to the database"""
    db_connection = sqlite3.connect(app.config['DATABASE'])
    db_connection.row_factory = sqlite3.Row
    return db_connection


def get_db_connection():
    if not hasattr(g, 'db_connection'):
        g.db_connection = connect_db()
    db_connection = g.db_connection
    return db_connection


@app.teardown_appcontext
def close_db(exception):
    """auto close the db after each request"""
    if hasattr(g, 'db_connection'):
        g.db_connection.close()


def verify_user(username, password):
    db_connection = get_db_connection()
    password_md5 = hashlib.md5(password).hexdigest()
    try:
        cursor = db_connection.execute(
                "select * from userlog where name = ? and password = ?",
                (username.decode('utf-8'), password_md5))
        rv = cursor.fetchone()
    finally:
        cursor.close()
    return rv is not None


def has_user(username):
    db_connection = get_db_connection()
    try:
        cursor =db_connection.execute(
                "select * from userlog where name = ?",
                (username.decode('utf-8'),))
        rv = cursor.fetchone()
    finally:
        cursor.close()
    return rv is not None


def submit_user(username, password):
    db_connection = get_db_connection()
    password_md5 = hashlib.md5(password).hexdigest()
    db_connection.execute(
        "INSERT INTO userlog (name,password,nowphase) VALUES (?,?,?)",
        (username.decode('utf-8'), password_md5, 0))
    db_connection.commit()
