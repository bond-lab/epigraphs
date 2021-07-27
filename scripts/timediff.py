import collections
from collections import defaultdict as dd
import sqlite3, sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
plt.style.use('seaborn-whitegrid')
#plt.style.use('grayscale')
###plt.rcParams['image.cmap'] = 'gray'

dbfile = "docs/epigraph.db"
conn = sqlite3.connect(dbfile)    # loads dbfile as con
c = conn.cursor()

def ncolor (nationality):
    if nationality in ('American', 'US'):
        return 'red'
    elif nationality in ('British', 'Irish', 'English', 'Scottish'):
         return 'blue'
    else:
        return 'black'
    
def nshape (nationality):
    if nationality in ('American', 'US'):
        return '*'
    elif nationality in ('British', 'Irish', 'English', 'Scottish'):
         return 'x'
    else:
        return '.'

def timediff (WFROM,WTO,efrom, eto, future=True, color=True):
    if future: ### allow citations into the future 
        c.execute("""
        SELECT wyear, eyear, count (eyear), wnationality
        FROM clean 
        WHERE (eyear IS NOT Null) AND (wyear IS NOT Null)
        AND WYEAR >= ? and WYEAR <= ? 
        AND eyear >= ? AND eyear <= ? 
        GROUP BY wyear, eyear
        ORDER BY wyear, eyear""", (WFROM, WTO, efrom, eto))
    else:
        c.execute("""
        SELECT wyear, eyear, count (eyear), wnationality
        FROM clean 
        WHERE (eyear IS NOT Null) AND (wyear IS NOT Null)
        AND WYEAR >= ? and WYEAR <= ? 
        AND eyear >= ? AND eyear <= ? 
        AND wyear > eyear
        GROUP BY wyear, eyear
        ORDER BY wyear, eyear""", (WFROM, WTO, efrom, eto))
    years = c.fetchall()
    epigraphtotal = sum (s for (x,y,s,n) in years)
    plt.xlim(WFROM, WTO)
    plt.ylim(efrom, eto)
    if color:
        plt.scatter([int(x) for (x,y,s,n) in years],
                    [int(y) for (x,y,s,n) in years],
                    s=[int(s) for (x,y,s,n) in years],
                    color=[ncolor(n) for (x,y,s,n) in years],
                    marker='.');
    else:
        plt.scatter([int(x) for (x,y,s,n) in years],
                    [int(y) for (x,y,s,n) in years],
                    s=[int(s) for (x,y,s,n) in years],
                    c='black',
                    marker='.');
        # uk = [ (x,y,s,n) for  (x,y,s,n) in years if ncolor(n) == 'blue']
        # plt.scatter([int(x) for (x,y,s,n) in uk],
        #             [int(y) for (x,y,s,n) in uk],
        #             s=[int(s) for (x,y,s,n) in uk],
        #             c='black',
        #             marker='x');
        # us = [ (x,y,s,n) for  (x,y,s,n) in years if ncolor(n) == 'red']
        # plt.scatter([int(x) for (x,y,s,n) in us],
        #             [int(y) for (x,y,s,n) in us],
        #             s=[int(s) for (x,y,s,n) in us],
        #             c='black',
        #             marker='*');

 
    
    plt.xlabel('Year of Work')
    plt.ylabel('Year of Epigraph')
    plt.title(f'Year of Epigraph vs Year of Work ({epigraphtotal} epigraphs)')
    plt.savefig(f"figs/eg-timediff-{WFROM}:{WTO}-{efrom}:{eto}-{future}-{color}.png")
    plt.close()

def generation(x, g):
    """return how many generations have passed"""
    return int(x/g)

def rat(d,n):
    if d == 0:
        return 0
    elif n ==0:
        print('n=', d , n)
    else:
        return d/n
    
def forebears (WFROM,WTO,efrom, eto, g=25):
    """graph the average distance back people cite
    g is the generation size
"""
    
    c.execute("""
    SELECT wyear, eyear, count (eyear), wnationality
    FROM clean 
    WHERE (eyear IS NOT Null) AND (wyear IS NOT Null)
    AND WYEAR >= ? and WYEAR <= ? 
    AND eyear >= ? AND eyear <= ? 
    GROUP BY wyear, eyear
    ORDER BY wyear, eyear""", (WFROM, WTO, efrom, eto))

    years = c.fetchall()
    epigraphtotal = sum (s for (x,y,s,n) in years)
    #plt.xlim(WFROM, WTO)
    #plt.ylim(100, -1500)
    #colors = list(mcolors.TABLEAU_COLORS.keys()) *20
    #print(colors)
    
    
    gen =dd(lambda: dd(int))
    gentotal= dd(int)
    for (x,y,s,n) in years:
        gen[generation(x,g)][generation(y-x,g)] += 1
        gentotal[generation(x,g)] +=1
        
    for x in gen:
        for y in gen[x]:
            print(x, y, gen[x][y], gentotal[x])

    

    plt.figure(figsize=(10, 5))
    ax=plt.axes()


    #df.plot(colormap=gray)        
    cumtotal = [0]*len(gen)

    for d in range(0,-200, -1):
              #for d in range(min(gen.keys()),max(gen.keys()),-1):
        xv = list(gen.keys())
        yv = [rat(gen[x][d],gentotal[x]) for x in xv]
        plt.bar(xv, yv, bottom=cumtotal,
                tick_label=[x*g for x in xv])
        cumtotal = [x + y for x, y in zip(yv, cumtotal)]
        #colors.pop()
        #print(d, cumtotal)
    plt.xlabel('Year of Work (in generations)')
    plt.ylabel(f'Share of Distance to forebear (in {g} year generations)')
    plt.title(f'Distance back vs Year of Work ({epigraphtotal} epigraphs)')
    plt.savefig(f"figs/eg-forebear-{WFROM}:{WTO}-{efrom}:{eto}-{g}.png")
    plt.close()

#        plt.bar(gen.keys(), gen[x][1].values()),bottom=gen[x][0].values()))
            
    # plt.scatter([int(x) for (x,y,s,n) in years],
    #             [int((y-x)) for (x,y,s,n) in years],
    #             s=[int(s) for (x,y,s,n) in years],
    #             color=[ncolor(n) for (x,y,s,n) in years]);
    # plt.title(f'Distance back vs Year of Work ({epigraphtotal} epigraphs)')
    # plt.savefig(f"figs/eg-forebear-{WFROM}:{WTO}-{efrom}:{eto}.png")
    # plt.close()

   

def timelen (WFROM, WTO):
    # for characters: avg(length(epigraph))
    c.execute("""
    SELECT wyear, avg(length(trim(epigraph)) - length(replace(trim(epigraph), ' ', '')) + 1)
    FROM clean 
    WHERE wyear IS NOT Null
    AND WYEAR >= ? and WYEAR <= ? 
    GROUP BY wyear
    ORDER BY wyear, wyear""", (WFROM, WTO))

    years = c.fetchall()

    c.execute ("""SELECT count(wyear)   
    FROM clean 
    WHERE wyear IS NOT Null
    AND WYEAR >= ? and WYEAR <= ?""", (WFROM, WTO))
    
    epigraphtotal,  = c.fetchone()

    plt.xlim(WFROM, WTO)
    xd =  [int(x) for (x,y) in years]
    yd =  [int(y) for (x,y) in years]
    par = np.polyfit(xd, yd, 1, full=True)
    slope=par[0][0]
    intercept=par[0][1]
    yl = [slope*xx + intercept  for xx in xd]
    
    plt.scatter(xd,
                yd,
                color='black');
    plt.plot(xd, yl)
    plt.xlabel('Year of Work')
    plt.ylabel('Epigraph Length')
    plt.title(f'Average Length of Epigraph (in words) vs \n Year of Work (for {epigraphtotal} epigraphs), from {WFROM} to {WTO}')
    plt.savefig("figs/eg-year-length.png")
    plt.close()

timediff(1650,2020,-500,2020)
timediff(1900,2020,1500,2020)
timediff(1650,2020,-500,2020, future=False)
timediff(1900,2020,1500,2020, future=False)
timediff(1900,2020,1500,2020, future=False, color=False)
# forebears(1650,2020,-500,2020)
forebears(1800,2020,-500,2020)
# forebears(1900,2020,-500,2020)
# forebears(1600,2020,-500,2020,g=50)
# forebears(1800,2020,-500,2020,g=50)
# forebears(1900,2020,-500,2020,g=50)

# timelen(1650,  2020)
