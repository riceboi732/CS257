CREATE TABLE olympians (id integer, name text, sex text, age integer, height float, weight float, team text, NOC text, medals text);
CREATE TABLE sports_and_events (sport text, event text);
CREATE TABLE sports_events_and_olympians (name text, event text);
CREATE TABLE olympics (games text, year integer, season text, city text);
CREATE TABLE NOC_details (NOC text, region text, notes text);
CREATE TABLE olympians_olympics (name text, game text);

