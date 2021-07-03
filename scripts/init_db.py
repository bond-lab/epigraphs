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

f=open(f'{args.data_dir}/tables.sql')
script=f.read()
#print(script)
###
### Make tables
### 
try:
    c.executescript(script)
    sys.stderr.write('Creating epigraph tables\n\n')
except:
    e = sys.exc_info()[0]
    sys.stderr.write('Not creating epigraph tables\n\n')
    pass # handle the error
conn.commit()
