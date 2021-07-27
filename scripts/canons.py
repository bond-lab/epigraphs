from collections import defaultdict as dd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sqlite3
import Levenshtein 
mpl.rcParams['axes.spines.left'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
#mpl.rcParams['axes.spines.bottom'] = False

import pandas as pd

###
### Litlab merged lists
###

df = pd.read_excel('data/LitLab_ _ to 20th CE Books Lists (Merged).xlsx',
                   sheet_name='wiki_merged') 

dbfile = "docs/epigraph.db"
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()    # creates a cursor object that can perform SQL commands with c.execute("...")




epiY=(0.0, 0.0, 0.0, 1.0) #BW
epiY=(0.3, 0.7, 0.9, 0.8) #blue
epiN=(0.0, 0.0, 0.0, 0.5)
survive=(0.0, 0.0, 0.0, 0.1)
# (/ 233 255.0)0.9137254901960784

epi = dd(int)
nepi = dd(int)

for i, j in df.iterrows():
    # if str(j[5]) in "YN":
    #     print(i, j[0],
    #           j[1],  # title
    #           j[4],  # year
    #           j[5])  # epigraph Y/N
    try:
        year = int(j[4])
        if j[5] == 'Y': 
            epi[year] +=1
        elif j[5] == 'N':
            nepi[year] +=1
    except:
        #print("Warning bad year:", j[4], j[1])
        year = j[4]

    c.execute("""INSERT INTO canon
    (source, title, author, nationality, year, epigraph_p)
    VALUES (?,?,?,?,?,?)""",
              [j[0], j[1], j[2], j[3], year, j[5]])
conn.commit()

#canon[author][work] = (year, nationality, epigraph_p)
#bloom[author][work] = (age, region)
#epigraph[eauthor][ework] = (eyear, wyear, wtitle, wauthor)



startyear= 1500
years = range(startyear,1941)
yes  = [epi[y] for y in years]
no   = [nepi[y] for y in years]
for i,y in enumerate(years):
    if i == 0:
        cyes =  [ yes[i] ]
        cno =  [ no[i] ]
    else:
        cyes.append(cyes[i-1] +  yes[i])
        cno.append(cno[i-1] +  no[i])




        
plt.figure(figsize=(10, 5))
p1 = plt.bar(years, yes, color=epiY)
p2 = plt.bar(years, no, color=epiN,
             bottom=yes)
plt.ylabel('Numbers of Novels')
plt.xlabel('Year of Publication')
plt.title('Works with and without epigraphs')
plt.legend((p1[0], p2[0]), ('+Epigraph', '-Epigraph'))
#plt.yscale("log")
plt.savefig("figs/novel-epi.png")
plt.close()

plt.figure(figsize=(10, 5))
p1 = plt.bar(years, cyes, color=epiY)
p2 = plt.bar(years, cno,
             bottom=cyes, color=epiN)
plt.ylabel('Numbers of Novels')
plt.xlabel('Year of Publication')
plt.title('Works with and without epigraphs (cumulative)')
plt.legend((p1[0], p2[0]), ('+Epigraph', '-Epigraph'))
#plt.yscale("log")
#
plt.savefig("figs/novel-epi-cum.png")
plt.close()

plt.figure(figsize=(10, 5))
p1 = plt.bar(years, yes, color=epiY)
p2 = plt.bar(years, no,
             bottom=yes, color=epiN)
plt.ylabel('Numbers of Novels')
plt.xlabel('Year of Publication')
plt.title('Works with and without epigraphs (log scale)')
plt.legend((p1[0], p2[0]), ('+Epigraph', '-Epigraph'))
plt.yscale("log")
plt.savefig("figs/novel-epi-log.png")
plt.close()


plt.figure(figsize=(10, 5))
p1 = plt.bar(years, cyes, color=epiY)
p2 = plt.bar(years, cno,
             bottom=cyes, color=epiN)
plt.ylabel('Numbers of Novels')
plt.xlabel('Year of Publication')
plt.title('Works with and without epigraphs (log scale, cumulative)')
plt.legend((p1[0], p2[0]), ('+Epigraph', '-Epigraph'))
plt.yscale("log")
#plt.figure(figsize=(10, 5))
plt.savefig("figs/novel-epi-log-cum.png")
plt.close()


###
### Surviving Printed Titles for Great Britain and Dependencies from the Beginnings of Print in England to the year 1800, by Alain Veylit.
### http://estc.ucr.edu/ESTCStatistics.html

fh = open('ESTC.tsv')

estc = dd(int)

for l in fh:
    if l.startswith('#'):
        continue
    (yr, count) = l.strip().split('\t')
    #print(yr, count)
    try:
        year = int(yr)
        estc[year] = int(count)
    except: 
        "Warning bad year in merged:", yr
        
years = range(1473, 1800)
works = [estc[y] for y in years]
yes  = [epi[y] for y in years]
no   = [nepi[y] for y in years]


plt.figure(figsize=(10, 5))
p1 = plt.bar(years, works, color=survive)
p2 = plt.bar(years, yes, color=epiY)
p3 = plt.bar(years, no, bottom =yes, color=epiN)
plt.ylabel('Numbers of Printed Titles Surviving')
plt.xlabel('Year of Publication')
plt.title('ESTC')

plt.legend((p1[0], p2[0], p3[0]), ('Surviving', '+Epigraph', '-Epigraph'))
plt.yscale("log")
#plt.figure(figsize=(10, 5))
plt.savefig("figs/works-surviving.png")
plt.close()



WFROM = 1650
WTO   = 2020
EFROM = -500
ETO   = 2020 
#canon[author][work] = (year, nationality, epigraph_p)
#bloom[author][work] = (age, region)
#epigraph[eauthor][ework] = (eyear, wyear, wtitle, wauthor)

canon_d = dd(lambda: dd(tuple))
bloom_d = dd(lambda: dd(tuple))
epi_d = dd(lambda: dd(tuple))

c.execute("""
SELECT eauthor, etitle, eyear, wyear, wtitle, wauthor
FROM clean 
WHERE (eyear IS NOT Null) AND (wyear IS NOT Null)
    AND WYEAR >= ? and WYEAR <= ? 
    AND eyear >= ? AND eyear <= ? 
    ORDER BY wyear, eyear""", (WFROM, WTO, EFROM, ETO))


for eauthor, etitle, eyear, wyear, wtitle, wauthor in c:
    epi_d[eauthor][etitle] = (eyear, wyear, wtitle, wauthor)
    
c.execute("""
SELECT author, title, year, nationality, epigraph_p
FROM canon 
WHERE (year IS NOT Null) 
    AND year >= ? AND year <= ? 
    ORDER BY year, year""", (EFROM, ETO))

for author, title, year, nationality, e_p in c:
    if author:
        author=author.strip()
    canon_d[author][title] = (year, nationality, e_p)

c.execute("""
SELECT author, title, age, region, countries
FROM bloom""" )


for author, title, age, region, countries in c:
    bloom_d[author][title] = (age, region, countries)

canon_bloom = set(list(canon_d.keys()) + list(bloom_d.keys()))

print("In Bloom but not in LL:")
for a in set(bloom_d.keys()).difference(set(canon_d.keys())):
    print (a)
print('===')
print(len(bloom_d.keys()))
print(len(canon_d.keys()))
print(len(set(bloom_d.keys()).difference(set(canon_d.keys()))))

bloom_stats_a = dd(lambda: dd(int))
bloom_stats = dd(int)
bloom_stats_w = dd(int)


for a in canon_bloom:
    #print(a)
    if a in epi_d:
        cited = 'cited'
    else:
        cited = '-'
    if a in bloom_d:
        bloom = 'bloom'
    else:
        bloom = '-'
    bloom_stats_a[a][(cited, bloom)] += sum(1 for e in [epi_d[a][w] for w in epi_d[a]])
    bloom_stats_w[(cited, bloom)] += sum(1 for e in [epi_d[a][w] for w in epi_d[a]])
    bloom_stats[(cited, bloom)] += 1
    
    print (f"{bloom}\t{cited}\t'{a}'")

print('In canonical list, cited, in bloom')
for t in bloom_stats:
    print (t,  bloom_stats[t],sep='\t')

print('In canonical list, cited, in bloom, weighted')
for t in bloom_stats_w:
    print (t,  bloom_stats_w[t],sep='\t')

total = sum(x for x in bloom_stats.values())
total_w = sum(x for x in bloom_stats_w.values())



print(f"""
<table>
<tr>
<th>In Bloom</th>
<th>In Epigraph</th> 
<th>No. Authors</th>
<th></th>
<th>No. Epigraphs</th>
<th></th>
</tr>
<tr>
  <td>No</td>
  <td>No</td>
  <td>{bloom_stats['-', '-']}</td>
  <td>{bloom_stats['-', '-']/total:.1%}</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>No</td>
  <td>Yes</td>
  <td>{bloom_stats['cited','-']}</td>
  <td>{bloom_stats['cited','-']/total:.1%}</td>
  <td>{bloom_stats_w['cited','-']}</td>
  <td>{bloom_stats_w['cited','-']/total_w:.1%}</td>
</tr>
<tr>
  <td>Yes</td>
  <td>No</td>
  <td>{bloom_stats['-','bloom']}</td>
  <td>{bloom_stats['-','bloom']/total:.1%}</td>
  <td></td>
  <td></td>
</tr>
<tr>
  <td>Yes</td>
  <td>Yes</td>
  <td>{bloom_stats['cited','bloom']}</td>
  <td>{bloom_stats['cited','bloom']/total:.1%}</td>
  <td>{bloom_stats_w['cited','bloom']}</td>
  <td>{bloom_stats_w['cited','bloom']/total_w:.1%}</td>
</tr>
<tr>
  <td colspan='2'>Total</td>
  <td>{total}</td>
  <td></td>
  <td>{total_w}</td>
  <td></td>
</tr>
</table>
""")
