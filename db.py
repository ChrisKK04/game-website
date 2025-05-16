import sqlite3
from flask import g

# forming a connection to the database
def get_connection(): 
    con = sqlite3.connect("database.db") # form a connection to the database
    con.execute("PRAGMA foreign_keys = ON") # make rows secure
    con.row_factory = sqlite3.Row # make referencing columns with their names possible
    return con # return the connection

# INSERT, UPDATE, DELETE
def execute(sql, params=[]):
    con = get_connection() # form a connection
    result = con.execute(sql, params) # command execution (INSERT, UPDATE, DELETE)
    con.commit() # commiting the database changes
    g.last_insert_id = result.lastrowid # storing the id of the last added row
    con.close() # connection close

# ID of the last changed row
def last_insert_id():
    return g.last_insert_id # fetching the ID of the last added row

# SELECT
def query(sql, params=[]):
    con = get_connection() # form a connection
    result = con.execute(sql, params).fetchall() # fetch all of the relevant rows
    con.close() # close the connection
    return result # return the result