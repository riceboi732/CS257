TASK 1:
SELECT DISTINCT noc FROM NOC_details ORDER BY noc;

TASK 2:
SELECT DISTINCT name FROM olympians  WHERE team = 'Kenya' ORDER BY name;

TASK 3:
SELECT olympians.name, olympics.games, sports_events_and_olympians.event, olympians.medals FROM olympics,sports_events_and_olympians,
olympians,olympians_olympics WHERE olympians.name = 'Greg Louganis' AND olympians.name = olympians_olympics.name AND olympics.games = olympians_olympics.game AND medals IS NOT NULL AND olympians.name = sports_events_and_olympians.name ORDER BY year;

TASK 4:
SELECT noc, COUNT(olympians.medals = 'Gold') FROM olympians GROUP BY noc ORDER BY COUNT (olympians.medals = 'Gold') DESC;




***
\copy olympians_olympics from 'olympians_olympics.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy olympians from 'olympians.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy olympics from 'olympics.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy sports_and_events from 'sports_and_events.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy sports_events_and_olympians from 'sports_events_and_olympians.csv' DELIMITER ',' CSV NULL AS 'NA';
\copy noc_details from 'noc_regions.csv' DELIMITER ',' CSV NULL AS 'NA';
***
