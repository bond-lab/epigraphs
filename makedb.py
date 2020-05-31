from collections import defaultdict as dd
import sqlite3, sys
from Levenshtein import distance

epigraphfile= 'epigraph.tsv'

epigraph= dd(list)

dbfile = "epigraph.db"
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()    # creates a cursor object that can perform SQL commands with c.execute("...")

f=open('tables.sql')
script=f.read()
#print(script)
###
### Make tables
### 
try:
    c.executescript(script)
    sys.stderr.write('Creating epigraph tables\n')
except:
    e = sys.exc_info()[0]
    sys.stderr.write('Not creating epigraph tables')
    pass # handle the error
conn.commit()

###
### read countries
###
country_idx = {}
f = open("countryInfo.txt")
for l in f:
    if l.startswith('#'):
        continue
    row = l.strip().split('\t')
    #print(row)
    #print(row[4], row[16], row[8], row[0])
    c.execute("""INSERT INTO country
    (name, geonameid, continent, iso)
    VALUES (?,?,?,?)""",
    (row[4], row[16], row[8], row[0]))
    country_idx[row[4]] = c.lastrowid

### FIXME get proper codes
more = [('England', 6269131, 'EU', 'GB-ENG'),
        ('Scotland',  6269131, 'EU', 'GB-ENG'),
        ('Wales',  6269131, 'EU', 'GB-ENG'),
        ('Northern Island',  6269131, 'EU', 'GB-ENG'),
        ('Ancient Greece',   6269131, 'EU', 'GRC'),
        ('Ancient Rome',   6269131, 'EU', 'GRC')]
    
for l in  more:
    c.execute("""INSERT INTO country
    (name, geonameid, continent, iso)
    VALUES (?,?,?,?)""",
    (l))
    country_idx[l[0]] = c.lastrowid
conn.commit()
# Continent codes :
# AF : Africa			geonameId=6255146
# AS : Asia			geonameId=6255147
# EU : Europe			geonameId=6255148
# NA : North America		geonameId=6255149
# OC : Oceania			geonameId=6255151
# SA : South America		geonameId=6255150
# AN : Antarctica			geonameId=6255152


cmap = {'US':'United States',
        'UK':'United Kingdom',
        'Britain':'United Kingdom',
        'Rome':'Ancient Rome',
        'Roman':'Ancient Rome',
        'Greek':'Ancient Greece'}

###
# make nationality table
nationality = set()
         
##
## read epigraphs
##

work = dict()
epigraph = dict()
epi_id=1
author = set()

country = set()
#f = open("LitLab_ Epigraph Collection - Epigraph Catalogue 1.tsv")
f = open(epigraphfile)
#author_id = 1
author = dd(set)
#work = dd(dict)
# work[title]['year'] = 1999
# work[title]['medium'] = 1999
# work[title]['genre'] = 1999
# work[title]['medium'] = 1999
# work[title]['country'] = 1999
# work[title]['author'] = 1999

work = dict()
#work[id](title, author, year, country, medium, genre, chapter, comment, isbn)
work2id=dd(set)
#work2id[(title, author, year)]=set(id)    
work_id = 1
for l in f:
    #print(l)
    row = l.strip().split('\t')
    for x in range(20 - len(row)): #normalize to 20 columns
        row.append('')
    if len(row[1]) == 0:
        continue

    ### first the authors
    ## epigraph author
    author[row[2].strip()].add('')
    ## work author
    author[row[9].strip()].add(row[11].strip())

    nationality.add(row[11].strip())
    ### then the works
    ## epigraph work
    work[work_id] = (row[3].strip(), #source
                     row[2].strip(), # author
                     row[7].strip(), # year
                     row[5].strip(), # country
                     row[4].strip(), # medium
                     '', '', '', 
                     row[8].strip(), # isbn
    )
    work_id += 1
    ### citing work
    work[work_id] = (row[10].strip(), #source
                     row[9].strip(), # author
                     row[12].strip(), # year
                     '', # country
                     '', # medium
                     row[13].strip(), # genre
                     '', '', 
                     row[14].strip(), # isbn
    )
    work_id += 1    

    epigraph[epi_id] = (row[1].strip(), work_id -2, work_id -1)
    epi_id+=1
    
#     for c in row[5].split('/'):
#         c = c.strip()
#         if c in cmap:
#             c = cmap[c]
#         if c and c not in country_idx:
#             print("Warning: Unknown Country {}, in row {}".format(c, row[0]))
#     at = row[2].strip()
#     a_guess = False
#     if at.startswith('*'):
#         a_guess = True
#         at=at.lstrip('*')
#     author.add(at) # tgt author
    
#     aw = row[8].strip()
#     author.add(aw) # src author
#     ## author, souce, year, source, medium
#     #epigraph[row[1]].append((row[2], row[3], row[4], row[12], row[5], row[6]))

# for nat in nationality:
#     nat = nat.replace("/", "-")
#     nat = nat.replace(", ", "-")
#     nat = nat.replace("New-Zealand", "New Zealand")
#     for n in nat.split('-'):
#         print (n)

for wid in work:
    (title, auth, year, country, medium, genre, chapter, comment, isbn) = work[wid]
    c.execute("""INSERT INTO work
    (id, title, author_id, year, country_id, medium, genre, comment, isbn)
    VALUES (?,?,?,?,?,?,?,?,?)""",
              [wid, title, auth, year, country, medium, genre, comment, isbn])
conn.commit()
    
for epi in epigraph:
    (epi_text, src, tgt) = epigraph[epi]
    c.execute("""INSERT INTO epigraph
    (id, epi, work_id_src, work_id_tgt)
    VALUES (?,?,?,?)""",
              [epi, epi_text, src, tgt])
conn.commit()
  

print("STOP", file=sys.stderr)

authors = sorted(author, reverse=True)
clean_authors = author
variants = dd(set)
canonical = dict()
for i,a in enumerate(authors):
    for b in authors[i:]:
        if a == b:
            continue
        else:
            dist = distance(a,b)
            if dist <=1:
                clean_authors[a] = clean_authors[a].union(clean_authors[b])
                canonical[b] = a
                variants[a].add(b)
                del clean_authors[b]




    

# epi=open("tab-common.tex", 'w')    
# limit =15
# #print """"""
# print("""
# \\begin{table*}[tbp]
#   \\centering
#   \\begin{tabular}{rp{.7\\textwidth}l}
# """, file=epi)
# for i, e in enumerate(sorted(epigraph.keys(), key=lambda x: len(epigraph[x]),reverse=True)):
#     if i <= limit:
#         #print(e, len(epigraph[e]), epigraph[e][0])
#         print ('{} & {} & {} \\\\'.format(len(epigraph[e]),e, epigraph[e][0][0]), file=epi)
# print("""  \\end{tabular}
#   \\caption{The most common epigraphs}\label{tab:common}
# \\end{table*}
# """, file=epi)
# epi.close()
