###
### api for reading the db
###
from collections import defaultdict as dd
import sqlite3, sys

dbfile = "epigraph.db"
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()    # creates a cursor object that can perform SQL commands with c.execute("...")

def get_author():
    """
    returns:
      works --- a list of works written by the author
    


    """
    return works

if __name__ == "__main__":
    print("hi")
