import sqlite3
import argparse

parser = argparse.ArgumentParser(
    description='Load the list of authors from Bloom',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    'epi_db', help='epigraph database')
parser.add_argument(
    '--bloom_data', help='bloom tsv', default = 'bloom.tsv')
parser.add_argument(
    '--data_dir', default = 'data', help='directory with data')
args = parser.parse_args()

dbfile =  args.epi_db
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()    # creates a cursor object that can perform SQL commands with c.execute("...")

fh = open(f'{args.data_dir}/{args.bloom_data}')


r2c = {'Middle Ages':['Europe'],
       'Ancient India':['India'],
       'Ancient Greeks':['Greece'],
       'Hellenistic Greeks':['Greece']}


### Author and country for Ancient Near East?
       
       
def region2countries(region):
    if region in r2c:
        countries= r2c[region]
    else:
        countries = region.split(';')
    return countries


for l in fh:
    if l.startswith('#'):
        continue
    if "<h3>" in l:
        continue
    #print(l)
    (age, region, author, work) = l.strip().split('\t')[:4]

    c.execute("""INSERT INTO bloom
    (age, region, author, title, countries)
    VALUES (?,?,?,?,?)""",
              [age, region, author, work,
               ';'.join(region2countries(region))])
conn.commit()
