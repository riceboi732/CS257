"""Martin Bernard and Victor Huang"""
import flask 
import psycopg2
import argparse
import json 
import sys 

api = flask.Blueprint('', __name__)

def connect_to_database():
    """connect program to database using config.py"""
    #from config import password
    #from config import database
    #from config import user

    try:
        connection = psycopg2.connect(database='shootings', user='', password='')
        return connection
    except Exception as e:
        print(e)
        exit()
        
    return connection

def excute_query(cursor, query, check):
    try:
        cursor.execute(query, check)
        print('QUERY:', cursor.query.decode('utf-8'))
    except Exception as e:
        print(e)
        exit()
        
    return cursor.fetchall()


@api.route('/victims')
def get_victims():
    state = flask.request.args.get('state', 'all')
    min_year = flask.request.args.get('min_year', '1000')
    max_year = flask.request.args.get('max_year', '5000')
    min_age = flask.request.args.get('min_age', '-10000')
    max_age = flask.request.args.get('max_age', '10000')
    ethnicity = flask.request.args.get('ethnicity', 'all')
    armed = flask.request.args.get('armed', 'all')
    
    state_check = '%' + state + '%'
    min_year_check = int(min_year)
    max_year_check = int(max_year)
    min_age_check = min_age 
    max_age_check =  max_age 
    ethnicity_check = '%' + ethnicity + '%'
    armed_check = '%' + armed + '%'

    check = (state_check, min_age_check, max_age_check, ethnicity_check, armed_check, min_year_check, max_year_check, )
    
    query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.victim_ethnicity LIKE %s
                AND victims.armed_status LIKE %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    if state == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.victim_ethnicity = %s 
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        
        check = (min_age_check, max_age_check, ethnicity_check, armed_check, min_year_check, max_year_check, )

    elif state == 'all' and ethnicity == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        check = (min_age_check, max_age_check, armed_check, min_year_check, max_year_check, )

    elif state == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.victim_ethnicity = %s  
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        
        check = (min_age_check, max_age_check, ethnicity_check, min_year_check, max_year_check, )

    elif state == 'all' and ethnicity == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        check = (min_age_check, max_age_check, min_year_check, max_year_check, )

    elif ethnicity == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        check = (state_check, min_age_check, max_age_check, armed_check, min_year_check, max_year_check, )

    elif ethnicity == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        check = (state_check, min_age_check, max_age_check, min_year_check, max_year_check, )

    elif armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= CAST(%s AS int) AND victims.victim_age <= CAST(%s AS int)
                AND victims.victim_ethnicity = %s
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
        check = (state_check, min_age_check, max_age_check, ethnicity_check, min_year_check, max_year_check, )

    connection = connect_to_database()
    #cursor = excute_query(connection.cursor(), query, check)

    #Hardcoded for the assignment due on 2/24
    hardQuery = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name LIKE %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id  
                ORDER BY victims.incident_date;'''
    hardCheck = (state_check,)
    hardCursor = excute_query(connection.cursor(), hardQuery, hardCheck)

    victims_list = []

    for row in hardCursor:
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

    
    
@api.route('/victims/analyze/year/<state>')
def get_years_vis_data(state):
    pass

@api.route('/victims/analyze/ethnicity/<state>')
def get_ethnicity_vis_data(state):
    pass

@api.route('/victims/analyze/armed/<state>')
def get_armed_vis_data(state):
    pass

@api.route('/victims/analyze/gender/<state>')
def get_gender_vis_data(state):
    pass 

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Webapp')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    api.run(host=arguments.host, port=arguments.port, debug=True)

