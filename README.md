# epigraphs
An API for looking up the epigraph database (and code to make the database)

This contains code to convert the epigraph data created by the project
*Digital Mapping the Literary Epigraph: Quantitative analysis of
literary influence using network theory and thousands of epigraphs*
led by Graham Mathews from 2017 to 2020, funded by the MOE Tier 1
grant at Nanyang Technological University.  This code was written by
Francis Bond.  Data is licenced under CC BY, code under the MIT license.

### Citations

 * Francis Bond and and Graham Matthews (2018) [Toward An Epic Epigraph Graph](https://aclanthology.org/L18-1522/) 11th edition of the Language Resources and Evaluation Conference (LREC 2018) Miyazaki 

## Data

Versions of the excel sheet used to collect the data and various subsidiary files are in the directory [data](./data)

## Scripts

Scripts to take the CSV, convert it to a database, clean it a little,
and so forth are in the directory [scripts](./scripts).  Which script
does what are documented in the bash files.

 - `do.bash` produces the database
 - `do-figs.bash` produces figures for the *Enslish* paper
 - `do-www.bash`

## Documentation

The epigraphs are available in three formats:

 - the original spreadsheet (`.xlsx`)
 - a cleaned up sqlite3 database (`epigraph.db`)
  - this is compressed for download (`epigraph.db.7z`)
 - indexes of who cites whom
 

## Goals of this research

The investigators propose to use the epigraph (the quotation positioned at the start of many novels) as a clear empirical marker of literary influence between time periods and countries. We aim to build a corpus of approximately 20,000 epigraphs and thoroughly investigate the connections within this big data set using network theory. We will explore the resulting implications by constructing a digital map of the world that demonstrates the evolution of the novel and its influences.

### Research questions

 * What were the key moral, philosophical, and aesthetic influences on literature through the ages?
 * How do different national literatures influence one another and what does the global map of literary "soft power" look like?
 * In what ways does visualising literature as a network rather than a set of discreet objects alter our understanding of the history of literature?

The outcome of this research project is the very first digital map of literary influence.

---


### Install


$ sudo apt-get install -y python3-levenshtein