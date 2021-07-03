import sys
import argparse
import sqlite3
from collections import defaultdict as dd
import numpy as np
import pandas as pd
import re

parser = argparse.ArgumentParser(
    description='Load the data from XLS',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    'epi_db', help='epigraph database')
parser.add_argument(
    'epi_xls', help='epigraph excel')
parser.add_argument(
    '--data_dir', default = 'data', help='directory with data')
args = parser.parse_args()


dbfile = args.epi_db
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()  

df = pd.read_excel(f'{args.data_dir}/{args.epi_xls}',
                   sheet_name='Epigraphs') 

df.fillna('NULL', inplace=True)

raw = list()
for i in df.itertuples():
    raw.append(tuple(i[1:]))

for row in raw:
    (eid, epigraphtext, eauthor, etitle, emedium, ecountry, ecount,
     eyear, eisbn, epart,
     wauthor, wtitle, wnationality, wnat, wyear, wyears,
     wgenre, wisbn, wfname, remarks, wedition) = row[:21]
    try:
        c.execute("""INSERT INTO raw
        (eid, epigraph, eauthor, etitle, emedium, ecountry, ecount,
        eyear, eisbn, epart,
        wauthor, wtitle, wnationality, wyear,
        wgenre, wisbn, wfname, remarks, wedition)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  [eid, epigraphtext, eauthor, etitle, emedium, ecountry, ecount,
                   eyear, eisbn, epart,
                   wauthor, wtitle, wnationality, wnat, wyear, wyears,
                   wgenre, wisbn, wfname, remarks, wedition])
    except:
        print("WARNING could not load into RAW", row)


def check_year(year, eid):
    if year and year != 'NULL':
        try:
            year = int(year)
            if year > 2020:
                print (f"WARNING {eid}: year is after 2020:", year) 
            return(year)
        except:
            print (f"WARNING {eid}: year is not integer:", year) 
            return 'NULL'

def check_text(text, eid):
    clean = text
    try:
        clean = text.strip()
        clean = clean.replace('****', '')
        clean = clean.replace('***', '')
        clean = clean.replace('**', '')
        clean = clean.replace('    ', ' ')
        clean = clean.replace('   ', ' ')
        clean = clean.replace('  ', ' ')
    except:
        print (f"WARNING {eid} weird text:", text, clean, sep='\t')
        
    if text != clean:
        print (f"CLEANED {eid}:", text, clean, sep='\t') 
    return (clean)
        
for row in raw:
    (eid, epigraphtext, eauthor, etitle, emedium, ecountry, ecount,
     eyear, eisbn, epart,
     wauthor, wtitle, wnationality, wnat, wyear, wyears,
     wgenre, wisbn, wfname, remarks, wedition) = row[:21]
    eyear = check_year(eyear, eid)
    wyear = check_year(wyear, eid)
    eauthor =  check_text(eauthor, eid)
    wauthor =  check_text(wauthor, eid)
    etitle  =  check_text(etitle, eid)
    wtitle  =  check_text(wtitle, eid)
    try:
        c.execute("""INSERT INTO clean
        (eid, epigraph, eauthor, etitle, emedium, ecountry,
        eyear, eisbn, epart,
        wauthor, wtitle, wnationality, wyear,
        wgenre, wisbn, wfname, remarks, wedition)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  [eid, epigraphtext, eauthor, etitle, emedium, ecountry,
                   eyear, eisbn, epart,
                   wauthor, wtitle, wnationality, wyear,
                   wgenre, wisbn, wfname, remarks, wedition])
    except:
        print("WARNING could not load into CLEAN", row)


df = pd.read_excel('data/LitLab_ _ to 20th CE Books Lists (Merged).xlsx',
                   sheet_name='wiki_merged')

for i, j in df.iterrows():
    # if str(j[5]) in "YN":
    #     print(i, j[0],
    #           j[1],  # title
    #           j[4],  # year
    #           j[5])  # epigraph Y/N
    try:
        year = int(j[4])
    # status = j[5] or ''
    # if status == 'Y': 
    #     epi[year] +=1
    # elif status == 'N':
    #     nepi[year] +=1
    except:
        print(f"Warning bad year: '{j[4]}' '{j[1]}'  ")
        year = j[4]
    try:
        author= re.sub(r'^([A-Za-z]+), (.*)$', r'\2 \1', j[2])
        if author != j[2]:
            print(f"Changed '{j[2]}' to '{author}'")
    except:
        print(f"Warning bad author: '{j[4]}' '{j[1]}'  ")
        author = j[2]
        
    c.execute("""INSERT INTO canon
    (source, title, author, nationality, year, epigraph_p)
    VALUES (?,?,?,?,?,?)""",
              [j[0], j[1], author, j[3], year, j[5]])
conn.commit()










conn.commit()

