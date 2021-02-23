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
    state = flask.request.args.get('state', all)
    min_year = int(flask.request.args.get('min_year', -10000))
    max_year = int(flask.request.args.get('max_year', 10000))
    min_age = int(flask.request.args.get('min_age', -10000))
    max_age = int(flask.request.args.get('max_age', 10000))
    ethnicity = flask.request.args.get('ethnicity', all)
    armed = flask.request.args.get('armed', all)
    
    connection = connect_to_database
    cursor = execute_querey(connection.cursor, query, check)
    querey = "SELECT victims.incident_date, victims.victim_name, victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status FROM victim_state, victims, states WHERE states.name = %s AND victims.id = victim_state.victim_id AND state.id = victim_state.state_id AND victim.incident_date >= min_year AND victim.incident_date <= max_year AND victim.victim_age <= max_age AND victim.victime_age >= min_year"
    

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



