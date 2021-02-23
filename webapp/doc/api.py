"""Martin Bernard and Victor Huang"""
import flask 
import psycopg2
import json 
import sys 

api = flask.Flask(__name__)

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
        
    return connection

def excute_query(cursor, query, check):
    try:
        cursor.execute(query, check)
    except Exception as e:
        print(e)
        exit()
        
    return cursor.fetchall()


@api.route('/victims')
def get_victims():
    state = flask.request.args.get('state', 'all')
    min_year = int(flask.request.args.get('min_year', '1000'))
    max_year = int(flask.request.args.get('max_year', '5000'))
    min_age = int(flask.request.args.get('min_age', -10000))
    max_age = int(flask.request.args.get('max_age', 10000))
    ethnicity = flask.request.args.get('ethnicity', 'all')
    armed = flask.request.args.get('armed', 'all')


    check = (state, min_year, max_year, min_age, max_age, ethnicity, armed,)
    
    query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.victim_ethnicity = %s 
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''
    
    if state == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.victim_ethnicity = %s 
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif state == 'all' and ethnicity == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif state == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.victim_ethnicity = %s  
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif state == 'all' and ethnicity == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif ethnicity == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %s AND victims.victim_age <= %s 
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif ethnicity == 'all' and armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''

    elif armed == 'all':
        query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %s AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %s AND victims.victim_age <= %s
                AND victims.victim_ethnicity = %s
                AND victims.incident_date BETWEEN '01-01-%s' AND '12-31-%s' 
                ORDER BY victims.incident_date;'''


    connection = connect_to_database()
    cursor = excute_query(connection.cursor, query, check)

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

    return json.dump(victims_list)

    
    
@api.route('/victims/analyze/year/<state>')
def get_years_vis_data(state):
    pass

@api.route('/victims/analyze/ethnicity/<state>')
def get_ethnicity_vis_data(state):
    pass

@api.route('/victims/analyze/armed/<state>')
def get_armed_vis_data(state):
    pass

@api.route('/victims/analyze/gender/<state>'):
def get_gender_vis_data(state):
    pass 



