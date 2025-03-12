# A module for making handling queries easier

import sqlite3
from flask import g

def get_connection(): # this function establishes a connection to the database
    con = sqlite3.connect("database.db") # connecting
    con.execute("PRAGMA foreign_keys = ON") # makes sure references work correctly
    con.row_factory = sqlite3.Row # makes referencing columns possible with their names
    return con

def execute(sql, parameters = []): # updating the database (INSERT, UPDATE and DELETE)
    con = get_connection() # connection
    result = con.execute(sql, parameters) # executing the query
    con.commit() # commiting the changes
    g.last_insert_id = result.lastrowid # storing the id of the last row
    con.close() # closing the database

def query(sql, parameters = []): # SEARCH queries
    con = get_connection() # connection
    result = con.execute(sql, parameters).fetchall() # fetch the matching rows
    con.close() # closing the database
    return result

def last_insert_id(): # fetching the id of the last row
    return g.last_insert_id