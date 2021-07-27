### Initialize the database
###
### uses the schema in data/tables.sql
###
python scripts/init_db.py docs/epigraph.db

###
### Load and clean the DBs
###
### it loads
###    the epigraph xls
###    a list of 20th CE books taken from wikipedia  (data/LitLab_ _ to 20th CE Books Lists (Merged).xlsx)
###
### potential problems are written to standard out
### (in this case redirected to warnings.txt) 
###
python scripts/load-xls.py docs/epigraph.db  ELH\ RAs\ renamed.xlsx > warnings.log

###
### Add the list of authors and works from Harold Bloom's the Western Canon
### the list is in data/bloom.tsv
###  - age
###  - source (region or country)
###  - author
###  - work
###
python scripts/add-bloom.py docs/epigraph.db

###
### A script to check for issues in the DB, currently none found
###
### output to epi_fails.log
###
python scripts/check.py docs/epigraph.db

###
### Compress the database for download
###

7z a docs/epigraph.db.7z docs/epigraph.db

#python scripts/listall.py
#python scripts/timediff.py
#python scripts/canons.py
