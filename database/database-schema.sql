table1:
CREATE TABLE olympians (id integer, name text, sex text, age integer, height float, weight float, team text, NOC text, medals text);

table2:
CREATE TABLE sports_and_events (sport text, event text);

table3:
CREATE TABLE sports_events_and_olympians (name text, event text);

table4: 
CREATE TABLE olympics (games text, year integer, season text, city text);

table5:
CREATE TABLE NOC_details (NOC text, region text, notes text);

table6:
CREATE TABLE olympians_olympics (name text, game text);
