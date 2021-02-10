import sys
import argparse
import psycopg2
import json
import flask

app = flask.Flask(__name__)


def connect_to_database():
    from config import password
    from config import database
    from config import user

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()

def sort_query(query,connection):
    try:
        cursor = connection.cursor()
        this_query = query
        cursor.execute(this_query)
        return cursor
    except Exception as e:
        print(e)
        exit()

"""method that makes game list of dictionaries
{'id': id, 'year': year, 'season': season, 'city': city}
"""
def make_games_dictionaries(connection):
    query = """SELECT * FROM olympic_games
    ORDER BY year DESC;"""
    result_list = []
    cursor = sort_by_query(query, connection)
    for row in cursor:
        result_list.append[{'id': row[0], 'year': row[1], 'season': row[2], 'city': row[3]}]
    return result_list

"""method that makes nocs list of dictionaries
{'abbreviation': abbreviation, 'name': name}"""
def make_noc_dictionaries(connection):
    query = """SELECT DISTINCT noc, noc_full
    FROM nocs, noc_regions
    WHERE noc_regions.noc_abbreviation = nocs.noc
    ORDER BY noc;"""
    result_list = []
    cursor = sort_by_query(query, connection)
    for row in cursor:
        result_list.append[{'abbreviation': row[0], 'name': row[1]}]
    return result_list

"""method that makes athlete list of dictionaries
{'athlete_id': athlete_id, 'athlete_name': athlete_name, 'athlete_sex':athlete_sex, 'sport':sport, 'event':event, 'medal':medal
}"""
def make_athlete_dictionaries(connection, oly_game_id):
    query = """SELECT athlete_id, athlete_name, sex, sport_categories.wport_category, detailed_event, medal
    FROM athletes, main_events, detailed_events, medals, olympic_games
    WHERE athletes.athlete_id = main_events.athlete_id
    AND main_events.oly_game_id = """ + oly_game_id + """
    AND medals.medal_id = main_events.medal_ID
    AND detailed_events.detailed_event_id = main_events.detailed_event_id
    AND sport_categories.sport_category_id = main_events.sport_category_id;
    """

    """SELECT athletes.athlete_id, athlete_name, sex, sport_categories.sport_category, detailed_event, medal
    FROM athletes, main_events, detailed_events, medals, olympic_games, sport_categories
    WHERE athletes.athlete_id = main_events.athlete_id
    AND main_events.oly_game_id = 2
    AND medals.medal_id = main_events.medal_ID
    AND detailed_events.detailed_event_id = main_events.detailed_event_id
    AND sport_categories.sport_category_id = main_events.sport_category_id;"""

    result_list = []
    cursor = sort_by_query(query, connection)
    for row in cursor:
        result_list.append[{'athlete_id': row[0], 'athlete_name': row[1], 'athlete_sex': row[2], 'sport': row[3], 'event': row[4], 'medal': row[5]}]
    return result_list

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

@app.route('/games')
def get_games():
    """list of games dictionary sorted by year"""
    games_list = []
    connection = connect_to_database()
    for game in make_games_dictionaries(connection):
        games_list.append(game)
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    """list of nocs dictionary alphabetized by NOC abbreviation"""
    nocs_list = []
    connection = connect_to_database()
    for noc in make_noc_dictionaries(connection):
        nocs_list.append(noc)
    return json.dumps(nocs_list)

@app.route('/medalists/games/<games_id>')
def get_medalists():
    """list of medalist dictionaries of medalists in specified olympic games"""
    medalist_list = []
    connection = connect_to_database()
    noc = flask.request.args.get('noc')
    for medalist in make_athlete_dictionaries(connection):
        if noc is not None and noc != make_athlete_dictionaries(connection)['noc']:
            continue
        medalist_list.append(medalist)
    return json.dumps(medalist_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)