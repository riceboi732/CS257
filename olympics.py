#Author: Victor Huang, Silas Zhao

#!/usr/bin/env python3
"""
Author: Victor Huang, Silas Zhao

usage: python3 olympics.py [-h] [-n NOC [NOC ...]] [-gl][-ln]
These are commands of olympics in various situations:

optional arguments:
	-h, --help              
							show this help message and exit
	
	-n [NOC ...], --noc  [NOC ...]
							lists the names of all the athletes from a specified NOC.

	-gl --goldList
							Lists all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.

	-ln --listNOC
							Lists all the NOCs in alphabetical order by abbreviation. 
    Note:
	1. Multiple arguments of the same flag will be handled in OR logic
		ex. $  python3 books.py -t boys wild
			Boys and Sex, 2020, Peggy Orenstein (1961-)
			The Tenant of Wildfell Hall, 1848, Ann Bronte (1820-1849)
			A Wild Sheep Chase, 1982, Haruki Murakami(1949-)
	2. Multiple arguments of different flags will be handled in AND logic
		ex. $  python3 books.py -t boys -a Peggy Herman
			Peggy Orenstein:
				Boys and Sex, 2020, Peggy Orenstein (1961-)
			Herman:
 				(No book matches)
	3. All find options are case-insensitive.
	4. If there are illegal arguments, the program will print the default help message.
    TASK 1:
    SELECT DISTINCT noc FROM NOC_details ORDER BY noc;

    TASK 2:
    SELECT DISTINCT name FROM olympians  WHERE NOC= 'Kenya' ORDER BY name;

    TASK 3:
    SELECT olympians.name, olympics.games, sports_events_and_olympians.event, olympians.medals FROM olympics,sports_events_and_olympians,
    olympians,olympians_olympics WHERE olympians.name = 'Greg Louganis' AND olympians.name = olympians_olympics.name AND olympics.games = olympians_olympics.game AND medals IS NOT NULL AND olympians.name = sports_events_and_olympians.name ORDER BY year;

    TASK 4:
    SELECT noc, COUNT(olympians.medals = 'Gold') FROM olympians GROUP BY noc ORDER BY COUNT (olympians.medals = 'Gold') DESC;

    """

import psycopg2
import config
import sys
import argparse
from config import password
from config import database
from config import user

def get_arguments():
    """
    Get argument from command line
    :return: args object
    """
    parser = argparse.ArgumentParser(prog="python3 olympics.py",
                                     description='manipulating olympics database')
    # Accessed by args.title

    parser.add_argument('-n', '--noc', type=str, nargs='+',
                        help='lists the names of all the athletes from a specified NOC.')
    # Accessed by args.author type=bool, nargs='+',
    parser.add_argument('-gl', '--gold_list',action='store_true',
                        help='Lists all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.')
    # Accessed by args.year
    parser.add_argument('-ln', '--list_NOC', action='store_true',
                        help='Lists all the NOCs in alphabetical order by abbreviation. ')                    

    args = parser.parse_args()

    return args
# Connect to the database

def get_noc(args,connection):
    """
    Get books published between two year arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects published between two year arguments
    """
    if not args.noc: 
        return
    if len(args.noc) > 1 or len(args.noc) == 0:
        print("please enter only one noc")
        exit()
    try:
        cursor = connection.cursor()
        query = '''SELECT DISTINCT name FROM olympians  WHERE NOC = %s ORDER BY name;'''
        search_string = args.noc[0]
        cursor.execute(query,(search_string,))
    except Exception as e:
        print(e)
        exit()

    # We have a cursor now. Iterate over its rows to print the results.
    print("lists the names of all the athletes from {0}".format(args.noc[0]))
    for row in cursor:
        print(row[0])


def get_gold_list(args,connection):
    if not args.gold_list:
        return

    try:
        cursor = connection.cursor()
        query = "SELECT noc, COUNT(olympians.medals = 'Gold') FROM olympians GROUP BY noc ORDER BY COUNT (olympians.medals = 'Gold') DESC;"
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

   
    for row in cursor:
        print(row[0], row[1])
    print()


def get_listNOC(args,connection):
    if not args.list_NOC:
        return

    try:
        cursor = connection.cursor()
        query = 'SELECT DISTINCT noc FROM noc_details ORDER BY noc;'
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # We have a cursor now. Iterate over its rows to print the results.
    print('List NOCs')
    for row in cursor:
        print(row[0])
    print()
def main():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    args = get_arguments()
    get_noc(args,connection)
    get_gold_list(args,connection)
    get_listNOC(args,connection)
    # Don't forget to close the database connection.
    connection.close()
main()

