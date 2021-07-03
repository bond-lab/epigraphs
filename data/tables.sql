CREATE TABLE raw (
-- raw data
-- store the entire csv as a database
-- known bad entries filtered out
eid 	 INTEGER,
epigraph TEXT,
eauthor  TEXT, -- (Last name, First name)
etitle  TEXT, 
emedium  TEXT, --  of Epigraph (Novel, Play, Song etc)
ecountry TEXT, -- if applicable
ecount TEXT, -- simplified if applicable
eyear 	 INTEGER, -- if applicable
eisbn	 TEXT,
epart 	 TEXT, -- 1 if chapter or part epigraph (Y/N in csv)
wtitle	 TEXT,
wauthor	 TEXT, -- (Last name, First Name)
wnationality	TEXT,
wnat TEXT,
wyear	 INTEGER,  --  year of  Original Publication
wyears INTEGER,
wgenre	 TEXT,
wisbn	 TEXT,
wfname	 TEXT, -- File name of Epigraph Photo (initial_filename) TEXT,
wedition TEXT, -- (if applicable)
remarks  TEXT
);

CREATE TABLE clean (
-- clean data
-- store the entire csv as a database
-- known bad entries filtered out
eid 	 INTEGER,
epigraph TEXT,
eauthor  TEXT, -- (Last name, First name, cleaned)
etitle  TEXT, 
emedium  TEXT, --  of Epigraph (Novel, Play, Song etc)
ecountry TEXT, -- if applicable
eyear 	 INTEGER, -- if applicable
eisbn	 TEXT,
epart 	 TEXT, -- 1 if chapter or part epigraph (Y/N in csv)
wtitle	 TEXT,
wauthor	 TEXT, -- (Last name, First Name)
wnationality	TEXT,
wyear	 INTEGER,  --  year of  Original Publication
wgenre	 TEXT,
wisbn	 TEXT,
wfname	 TEXT, -- File name of Epigraph Photo (initial_filename) TEXT,
wedition TEXT, -- (if applicable)
remarks  TEXT
);
--- works
CREATE TABLE work (
id INTEGER primary key,
isbn INTEGER,
-- from text
source TEXT,
-- normalized
title TEXT,
author_id INTEGER,
year INTEGER,
country_id INTEGER,
medium TEXT,
genre TEXT,
chapter TEXT,
comment INTEGER
);
--- work_country
CREATE TABLE work_country (
id INTEGER primary key,
work_id INTEGER,
country_id INTEGER,
comment INTEGER
);
--- the author
CREATE TABLE author (
id  primary key,
name TEXT,
dob DATE,
dod DATE
nat_id INTEGER,
comment TEXT
);
--- nationality
CREATE TABLE nat (
id primary key,
name TEXT,
comment TEXT
);
--- nat_country (
CREATE TABLE nat_country (
id primary key,
nat_id INTEGER,
country_id INTEGER,
comment TEXT
);

--- the epigraph
CREATE TABLE country (
id INTEGER primary key,
name TEXT,
geonameid INTEGER,
continent TEXT,
iso TEXT,
comment TEXT
);
--- the epigraph
CREATE TABLE epigraph (
id INTEGER primary key,
epi TEXT,
--- works
work_id_src INTEGER,
work_id_tgt INTEGER,
--- variant of epigraph
can INTEGER,
comment TEXT
);

--- bloom
CREATE TABLE bloom (
id  INTEGER primary key,
age  TEXT,
region TEXT,
author TEXT,
title TEXT,
author_id INTEGER,
work_id INTEGER,
countries TEXT);

--- canon
CREATE TABLE canon (
id  INTEGER primary key,
source  TEXT,
title TEXT,
author TEXT,
year INTEGER,
nationality TEXT,
epigraph_p TEXT, 
author_id INTEGER,
work_id INTEGER,
countries TEXT);
