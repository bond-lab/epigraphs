from collections import defaultdict as dd
import sqlite3, sys

import argparse

parser = argparse.ArgumentParser(
    description='List all the authors and who cites whom',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    'epi_db', help='epigraph database')
parser.add_argument(
    '--www_dir', default = 'docs/epi', help='directory with data')
args = parser.parse_args()

dbfile =  args.epi_db
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()   




def link(author):
    return f"<a href='{author}.html' class='author'>{author}</a>"




cites = dd(lambda: dd(int))
cited = dd(lambda: dd(int))

c.execute ("""SELECT  eauthor, wauthor FROM clean""")
for (eauthor, wauthor) in c:
    cited[eauthor][wauthor] += 1
    cites[wauthor][eauthor] += 1

authors = sorted(set(list(cited.keys()) + list(cites.keys())))

f = open(f'{args.www_dir}/authors.html', 'w')
print("""<html>\n<body>""", file=f)
for a in authors:
    if a == '':
        a = 'None'
    print(f"<h3>Author: {link(a)}</h3>", file=f)
    print("<ul>", file=f)
    if a in cites:
        print (f"<li>Cites", file=f)
        print("<ul>", file=f)
        for ca in cites[a]:
            print (f"<li>{ca} ({cites[a][ca]})", file=f)
        print("</ul>", file=f)
    if a in cited:
        print (f"<li>Cited by", file=f)
        print("<ul>", file=f)
        for ca in cited[a]:
            print (f"<li>{link(ca)} ({cited[a][ca]})", file=f)
        print("</ul>", file=f)
    print("</ul>", file=f)
print("""</body>\n</html>""", file=f)



cites_a = dd(lambda: dd(lambda: dd(list)))
cited_a = dd(lambda: dd(lambda: dd(list)))


c.execute("""SELECT eid, epigraph, eauthor, etitle,
     ecountry, eyear, emedium,
     wtitle, wauthor, wnationality,
     wyear, wgenre FROM clean""")

for (eid, epigraph, eauthor, etitle,
     ecountry, eyear, emedium,
     wtitle, wauthor, wnationality,
     wyear, wgenre) in c:
    cited_a[eauthor][wauthor][wtitle] = (eid, epigraph, etitle,
                                       ecountry, eyear, emedium,
                                       wnationality,
                                       wyear, wgenre)                  
    cites_a[wauthor][eauthor][wtitle] = (eid, epigraph, etitle,
                                       ecountry, eyear, emedium,
                                       wnationality,
                                       wyear, wgenre)                  

for a in authors:
    a = a.replace('/', ';')
    if a == '':
        a = 'None'
    f = open(f'{args.www_dir}/{a}.html', 'w')
    print("""<html>\n<body>""", file=f)
    print(f"<h1>Author: {a}</h1>", file=f)
    if a in cites:
        print (f"<h3>Cites</h3>", file=f)
        print("<ul>", file=f)
        for ca in cites_a[a]:
            print (f"<li>{link(ca)} ({cites[a][ca]})", file=f)
            print("<ul>", file=f)
            for work in cites_a[a][ca]:
                (eid, epigraph, etitle,
                 ecountry, eyear, emedium,
                 wnationality,
                 wyear, wgenre) = cites_a[a][ca][work]
                print(f"""<li>IN: <i>{work}</i> ({wyear}) {wgenre}, {wnationality  }
                <br>EPIGRAPH: <i><b>{epigraph}</i></b>
                <br>FROM: <i>{etitle}</i>,  ({eyear}), {emedium}, {ecountry}""",
                      file= f)
            print("</ul>", file=f)
        print("</ul>", file=f)
    if a in cited:
        print (f"<h3>Cited by</h3>", file=f)
        print("<ul>", file=f)
        for ca in cited[a]:
            print (f"<li>{link(ca)} ({cited[a][ca]})", file=f)
            print("<ul>", file=f)
            for work in cited_a[a][ca]:
                (eid, epigraph, etitle,
                 ecountry, eyear, emedium,
                 wnationality,
                 wyear, wgenre) = cited_a[a][ca][work]
                print(f"""<li>IN: <i>{work}</i> ({wyear}) {wgenre}, {wnationality  }
                <br>EPIGRAPH: <i><b>{epigraph}</i></b>
                <br>FROM: <i>{etitle}</i>,  ({eyear}), {emedium}, {ecountry}""",
                      file= f)
            print("</ul>", file=f)
  
        print("</ul>", file=f)
    print("""</body>\n</html>""", file=f)

# for a in authors:
#     a = a.replace('/', ';')
#     if a == '':
#         a = 'None'
#     f = open('www/index.html', 'w')   
#     print("""<html>\n<body>""", file=f)
#     print("<ul>", file=f)
#     print(f"  <li><a href='{a}.html'>{a}</a>", file=f)
#     print("</ul>", file=f)
#     print("""</body>\n</html>""", file=f)
