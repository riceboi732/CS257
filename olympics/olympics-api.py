"""Authors: Victor Huang, Kyosuke Imai"""
import argparse
import psycopg2
import json
import flask
import sys

app = flask.Flask(__name__)

def connect_to_database():
    """connect program to database using config.py"""
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
    """make cursor object for data sorted based on query"""
    try:
        cursor = connection.cursor()
        this_query = query
        cursor.execute(this_query)
        return cursor
    except Exception as e:
        print(e)
        exit()


def make_games_dictionaries(connection):
    """method that makes list of dictionaries for olympic games
    {'id': id, 'year': year, 'season': season, 'city': city}
    returns list of dictionaries
    """
    query = """SELECT * FROM olympic_games
    ORDER BY year DESC;"""
    result_list = []
    cursor = sort_query(query, connection)
    for row in cursor:
        result_list.append({'id': row[0], 'year': row[1], 'season': row[2], 'city': row[3]})
    return result_list


def make_noc_dictionaries(connection):
    """method that makes list of dictionaries for noc
    {'abbreviation': abbreviation, 'name': name}
    returns list of dictionaries"""
    query = """SELECT DISTINCT noc, noc_full
    FROM nocs, noc_regions
    WHERE noc_regions.noc_abbreviation = nocs.noc
    ORDER BY noc;"""
    result_list = []
    cursor = sort_query(query, connection)
    for row in cursor:
        result_list.append({'abbreviation': row[0], 'name': row[1]})
    return result_list


def make_athlete_dictionaries(connection, oly_game_id):
    """method that makes list of dictionaries for athletes
    {'athlete_id': athlete_id, 'athlete_name': athlete_name, 'athlete_sex':athlete_sex, 'sport':sport, 'event':event, 'medal':medal
    }"""
    query = """SELECT DISTINCT athletes.athlete_ID, athlete_name, sex, sport_category, detailed_event, medal
    FROM athletes, main_events, olympic_games, detailed_events, medals, sport_categories
    WHERE olympic_games.oly_game_ID = """ + oly_game_id + """
    AND olympic_games.oly_game_ID = main_events.oly_game_ID
    AND athletes.athlete_ID = main_events.athlete_ID
    AND detailed_events.detailed_event_id = main_events.detailed_event_id
    AND medals.medal_id = main_events.medal_id
    AND sport_categories.sport_category_id = main_events.sport_category_id
    AND (medal = 'Gold' OR medal = 'Silver' OR medal = 'Bronze'  )
    ;"""

    result_list = []
    cursor = sort_query(query, connection)
    for row in cursor:
        result_list.append({'athlete_id': row[0], 'athlete_name': row[1], 'athlete_sex': row[2], 'sport': row[3], 'event': row[4], 'medal': row[5]})
    return result_list

"""Creating the athlete list of dictionaries for methods below"""
def make_athlete_dictionaries_with_nocs(connection, oly_game_id, nocs):
    query = """SELECT DISTINCT athletes.athlete_ID, athlete_name, sex, sport_category, detailed_event, medal
    FROM athletes, main_events, olympic_games, detailed_events, medals, sport_categories, nocs
    WHERE olympic_games.oly_game_ID = """ + oly_game_id + """
    AND olympic_games.oly_game_ID = main_events.oly_game_ID
    AND athletes.athlete_ID = main_events.athlete_ID
    AND detailed_events.detailed_event_id = main_events.detailed_event_id
    AND medals.medal_id = main_events.medal_id
    AND sport_categories.sport_category_id = main_events.sport_category_id
    AND nocs.noc = '""" + nocs + """'
    AND nocs.nocs_id = main_events.noc_id
    AND (medal = 'Gold' OR medal = 'Silver' OR medal = 'Bronze'  )
    ; """


    result_list = []
    cursor = sort_query(query, connection)
    for row in cursor:
        result_list.append({'athlete_id': row[0], 'athlete_name': row[1], 'athlete_sex': row[2], 'sport': row[3], 'event': row[4], 'medal': row[5]})
    return result_list

@app.route('/')
def hello():
    return 'Hello, Welcome to our Olympics database!'

@app.route('/games')
def get_games():
    """returns json list of dictionaries of olympics games attributes"""
    games_list = []
    connection = connect_to_database()
    for game in make_games_dictionaries(connection):
        games_list.append(game)
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    """returns json list of dictionaries of noc attributes"""
    nocs_list = []
    connection = connect_to_database()
    for noc in make_noc_dictionaries(connection):
        nocs_list.append(noc)
    return json.dumps(nocs_list)


@app.route('/medalists/games/<games_id>')
def get_medalists_noc(games_id):
    """returns json list of dictionaries depending on argument"""
    medalist_list = []
    oly_game_id = games_id
    connection = connect_to_database()
    noc = flask.request.args.get('noc')
    string_noc = str(noc)

    if noc:
        for medalist in make_athlete_dictionaries_with_nocs(connection, oly_game_id, string_noc):
            medalist_list.append(medalist)
    else:
        for medalist in make_athlete_dictionaries(connection, oly_game_id):
            medalist_list.append(medalist)

    return json.dumps(medalist_list)





if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
