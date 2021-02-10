
"""Author: Kyosuke Imai
Simple command-line interface that takes in specfic SQL queries.
"""


import argparse
import psycopg2


def main():
    """takes in command line arguments and returns a sorted list of appropriate data"""
    connection = connect_to_database()
    arguments = get_command_line_arguments()
    if need_help(arguments):
        print_usage_txt()
    else:
        query, title = get_query(arguments)
        cursor = sort_by_user_query(query,connection)
        print_results(cursor, title, arguments)

    connection.close()

def connect_to_database():
    """connects program to database by pulling configuration data from config.py
    """
    from config import password
    from config import database
    from config import user

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()

def need_help(command_line_arguments):
    """@return: returns parser object of parsed command_line_arguments"""
    has_argument = command_line_arguments.athletes_noc or command_line_arguments.gold_nocs or command_line_arguments.year_athletes_gold
    if not has_argument or command_line_arguments.help:
        return True
    else:
        return False

def get_command_line_arguments():
    """ @return: returns query and query title based on command line argument input
        @param: parsed command line arguments"""
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument("--help", "-h", action = "store_true")
    parser.add_argument("--athletes_noc", "-a", type = str,  help = '' )
    parser.add_argument("--gold_nocs", "-b", action = "store_true")
    parser.add_argument("--year_athletes_gold", "-c", help  = ' ' )

    return parser.parse_args()


def get_query(command_line_arguments):
    """ @return: returns query and query title based on command line argument input
        @param: parsed command line arguments"""
    if command_line_arguments.athletes_noc:
        search_string = command_line_arguments.athletes_noc

        query = """SELECT DISTINCT athlete_name, Team
        FROM athletes, teams, main_events
        WHERE teams.Team LIKE '%""" + search_string + """%'
        AND teams.team_ID = main_events.team_ID
        AND athletes.athlete_ID = main_events.athlete_ID;
        """
        query_name = '===== Names of all Athletes from {0} ====='.format(search_string)
        return query, query_name

    if command_line_arguments.gold_nocs:
        query = """SELECT teams.Team, COUNT(medals.medal)
        FROM teams, medals, main_events
        WHERE teams.team_ID = main_events.team_ID
        AND medals.medal_ID = main_events.medal_ID
        AND medals.medal = 'Gold'
        GROUP BY teams.Team
        ORDER BY COUNT(medals.medal) DESC;
        """
        query_name = '===== all the NOCs + gold medals won, in decreasing order of the number of gold medals. ====='
        return query, query_name

    if command_line_arguments.year_athletes_gold:
        search_string = command_line_arguments.year_athletes_gold

        query = """SELECT athlete_name, year
        FROM athletes, medals, olympic_games, main_events
        WHERE athletes.athlete_ID = main_events.athlete_ID
        AND olympic_games.oly_game_ID = main_events.oly_game_ID
        AND medals.medal_ID = main_events.medal_ID
        AND olympic_games.year = ' """ + search_string + """'
        AND medals.medal = 'Gold';
        """
        query_name = '===== All athletes than won gold medals in {0} ====='.format(search_string)
        return query, query_name


def sort_by_user_query(query, connection):
    """@return: returns cursor object
        @param: String query
        @param: connection which connects program to the database"""
    try:
        cursor = connection.cursor()
        this_query = query
        cursor.execute(this_query)
        return cursor
    except Exception as e:
        print(e)
        exit()

def print_results(cursor, search_title, command_line_arguments):
    """print method that iterates through cursor object and prings the appropriate row
        @param: iterable curser object with sorted data
        @param: string for header of list
        @param: command line arguments
    """
    print(search_title)
    if command_line_arguments.athletes_noc:
        for row in cursor:
            print(row[0])
    if command_line_arguments.gold_nocs:
        for row in cursor:
            print('{:<20s}{:>20d}'.format(row[0],row[1]))
            #print("Country:", row[0], "  #of gold medals:".format(*row), row[1])
    if command_line_arguments.year_athletes_gold:
        for row in cursor:
            print(row[0])
    print()

def print_usage_txt():
    """print usage text with infomration on how to use command line interface"""
    for line in open('usage.txt').readlines():
        print(line, end='')


main()
