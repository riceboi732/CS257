RUBRIC:

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

\copy olympians_olympics from 'olympians_olympics.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy olympians from 'olympians.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy olympics from 'olympics.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy sports_and_events from 'sports_and_events.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy sports_events_and_olympians from 'sports_events_and_olympians.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy noc_details from 'noc_regions.csv' DELIMITER ',' CSV NULL AS 'NA';


