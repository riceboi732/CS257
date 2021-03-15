"""Martin Bernard and Victor Huang"""
import flask 
import psycopg2
import argparse
import json 
import sys 

api = flask.Blueprint('', __name__)

def connect_to_database():
    """Import the database information from config.py and connect to the database"""
    from config import password
    from config import database
    from config import user

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
        
    return connection

def excute_query(cursor, query, check):
    """Returns all the rows of the query result
    
    Parameters
        cursor: cursor object
        query: SQL query statement 
        check: Tuple that checks for SQL injections
    """
    try:
        cursor.execute(query, check)
        print('QUERY:', cursor.query.decode('utf-8'))
    except Exception as e:
        print(e)
        exit()
        
    return cursor.fetchall()


@api.route('/victims')
def get_victims():
    """Return a JSON list of dictionaries based on the given query"""

    #Assign the GET paramters and set their default
    state = flask.request.args.get('state', 'all')
    min_year = flask.request.args.get('min_year', '1000')
    max_year = flask.request.args.get('max_year', '5000')
    min_age = flask.request.args.get('min_age', '0')
    max_age = flask.request.args.get('max_age', '1000')
    ethnicity = flask.request.args.get('ethnicity', 'all')
    armed = flask.request.args.get('armed', 'all')
    search = flask.request.args.get('search', 'none')
    
    #Adds % around the GET parameters to check for SQL injection 
    state_check = '%' + state + '%'
    min_year_check = int(min_year)
    max_year_check = int(max_year)
    min_age_check = min_age 
    max_age_check =  max_age 
    ethnicity_check = '%' + ethnicity + '%'
    armed_check = '%' + armed + '%'
    search_check = '%' + search + '%'

    #Variable to make sure that the armed status is returned properly because "armed" is present in both "armed" and "unarmed"
    if armed == 'armed':
        armed_start = 'a%'
    else:
        armed_start = 'u%'
    
    #Create the check variable and query based on the given parameters
    #Other parameters are only called when the search parameter is its default value 
    if search == 'none':

        #the value of the state parameter is its default value 
        if state == 'all' and ethnicity != 'all' and armed != 'all':
            check = (min_age_check, max_age_check, ethnicity_check, armed_check, armed_start, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.victim_ethnicity LIKE %s
                    AND victims.armed_status LIKE %s 
                    AND victims.armed_status LIKE %s
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #the value of the state and the ethnicity parameters are their default value
        elif state == 'all' and ethnicity == 'all' and armed != 'all':
            check = (min_age_check, max_age_check, armed_check, armed_start, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.armed_status LIKE %s
                    AND victims.armed_status LIKE %s
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #the value of the state and the armed parameters are their default value
        elif state == 'all' and ethnicity != 'all' and armed == 'all':
            check = (min_age_check, max_age_check, ethnicity_check, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.victim_ethnicity LIKE %s
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #state, ethnicity, and armed parameters all have default values 
        elif state == 'all' and ethnicity == 'all' and armed == 'all':
            check = (min_age_check, max_age_check, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #the value of the ethnicity parameter is its default value 
        elif state != 'all' and ethnicity == 'all' and armed != 'all':
            check = (state_check, min_age_check, max_age_check, armed_check, armed_start, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.armed_status LIKE %s
                    AND victims.armed_status LIKE %s 
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #ethnicity and armed parameters have default values  
        elif state != 'all' and ethnicity == 'all' and armed == 'all':
            check = (state_check, min_age_check, max_age_check, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #armed parameter have default values
        elif state != 'all' and ethnicity != 'all' and armed == 'all':
            check = (state_check, min_age_check, max_age_check, ethnicity_check, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                    AND victims.victim_ethnicity LIKE %s
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
        
        #state, ethnicity, and armed parameters are given 
        else:
            check = (state_check, min_age_check, max_age_check, ethnicity_check, armed_check, armed_start, min_year_check, max_year_check, )
        
            query = '''SELECT victims.incident_date, victims.victim_name, 
                    victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                    FROM victim_state, victims, states 
                    WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                    AND victims.victim_ethnicity LIKE %s
                    AND victims.armed_status LIKE %s 
                    AND victims.armed_status LIKE %s 
                    AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                    ORDER BY victims.incident_date;'''
    else:
        #state parameter is its default value and search parameter is given 
        if state == 'all':
            check = (search_check, )

            query = '''SELECT victims.incident_date, victims.victim_name, victims.victim_age, victims.victim_gender, 
                    victims.victim_ethnicity, victims.armed_status, states.state_name
                    FROM victim_state, victims, states
                    WHERE victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND victims.victim_name LIKE %s
                    ORDER BY victims.incident_date;
                   '''
        #both state and search parameters are given 
        else:
            check = (state_check, search_check, )

            query = '''SELECT victims.incident_date, victims.victim_name, victims.victim_age, victims.victim_gender, 
                    victims.victim_ethnicity, victims.armed_status, states.state_name
                    FROM victim_state, victims, states
                    WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                    AND lower(victims.victim_name) LIKE lower(%s) 
                    ORDER BY victims.incident_date;
                    '''

    #Connect to database and excute query
    connection = connect_to_database()
    cursor = excute_query(connection.cursor(), query, check)

    #Loops through the rows in query and create a list of dictionary to return 
    victims_list = []

    for row in cursor:
        date = row[0]
        name = row[1]
        age = row[2]
        gender = row[3]
        ethnicity = row[4]
        armed = row[5]
        state = row[6]

        victims_list.append({'date': date, 'name': name, 'age': age, 'gender': gender, 'ethnicity': ethnicity, 'armed': armed, 'state': state})
    
    connection.close()

    return json.dumps(victims_list, indent=4, default=str)
    
@api.route('/victims/analyze/<state_ab>')
def get_vis_data(state_ab):
    """Return a list of a JSON list of all victims from the given state"""

    #Assign default values to GET parameters
    state = state_ab
    min_year = 1000
    max_year = 5000
    min_age = '0'
    max_age = '1000'
    
    #Check for SQL injection given the state parameter 
    state_check = '%' + state + '%'

    check = (state_check, min_age, max_age, min_year, max_year, )
    
    query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age BETWEEN CAST(%s AS int) AND CAST(%s AS int)
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
    
    connection = connect_to_database()
    cursor = excute_query(connection.cursor(), query, check)

    #Create a list of dictionaries to return 
    victims_list = []

    for row in cursor:
        date = row[0]
        name = row[1]
        age = row[2]
        gender = row[3]
        ethnicity = row[4]
        armed = row[5]
        state = row[6]

        victims_list.append({'date': date, 'name': name, 'age': age, 'gender': gender, 'ethnicity': ethnicity, 'armed': armed, 'state': state})
    
    connection.close()

    return json.dumps(victims_list, indent=4, default=str)

@api.route('/api/help')
def get_api_help():
    """Renders the api_help.html file which has instructions on how to use the API"""
    return flask.render_template('api_help.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Webapp')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    api.run(host=arguments.host, port=arguments.port, debug=True)

