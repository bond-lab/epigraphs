### Initialize the database
###
### uses the schema in data/tables.sql
###
python scripts/init_db.py www/epigraph.db

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
python scripts/load-xls.py www/epigraph.db  ELH\ RAs\ renamed.xlsx > warnings.txt


python scripts/add-bloom.py www/epigraph.db
python scripts/check.py epigraph.db
python scripts/listall.py
python scripts/timediff.py
python scripts/canons.py
