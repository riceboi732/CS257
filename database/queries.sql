SELECT DISTINCT noc FROM NOC_details ORDER BY noc;
SELECT DISTINCT name FROM olympians  WHERE team = 'Kenya' ORDER BY name;
SELECT olympians.name, olympics.games, sports_events_and_olympians.event, olympians.medals FROM olympics,sports_events_and_olympians,
olympians,olympians_olympics WHERE olympians.name = 'Greg Louganis' AND olympians.name = olympians_olympics.name AND olympics.games = olympians_olympics.game AND medals IS NOT NULL AND olympians.name = sports_events_and_olympians.name ORDER BY year;
SELECT noc, COUNT(olympians.medals = 'Gold') FROM olympians GROUP BY noc ORDER BY COUNT (olympians.medals = 'Gold') DESC;
