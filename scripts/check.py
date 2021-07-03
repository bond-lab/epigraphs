import sys
import argparse
import sqlite3
from collections import defaultdict as dd

parser = argparse.ArgumentParser(
    description='Initialize the Epigraph Database',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    'epi_db', help='epigraph database')
parser.add_argument(
    '--data_dir', default = 'data', help='directory with data')
args = parser.parse_args()


dbfile = args.epi_db
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()  

log = open("epi_fails.log", 'w')

c.execute("""select eid, eyear, wyear, etitle, wtitle from raw where eyear > wyear and eyear != 'NULL' and wyear != 'NULL';""")
print ("""Epigraph year is after work year""", file=log)
print("ID", "Epigraph Year", "Work year", "Source", "work",
      sep='\n', file=log)
print("\n", file=log)
for r in c:
    print(f"""{str(r[0])}
{str(r[1])}\t{str(r[3])}   
{str(r[2])}\t{str(r[4])}
""", file=log)

print("\n-----------------------------\n", file=log)




conn.commit()
