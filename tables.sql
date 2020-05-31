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


