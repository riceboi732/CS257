"""Martin Bernard and Victor Huang"""
import flask 
import psycopg2
import json 
import sys 

app = flask.Flask(__name__)

def connect_database():
    pass 

def excute_query(cursor, query):
    pass 

app.route('/victims')
def get_victims():
    """
    REQUEST: /victims 
    
    GET parameters: 
        state(Optinal, default: all states): Only return victims from the specified states
        min_year(Optional, default: -10000): Only return victims that are equal to or greater this year
        max_year(Optional, default: 10000): Only return victims that are equal or less than this year 
        min_age(Optional, default: -1000): Only return victims that are equal or older than this age
        max_age(Optional, default: 1000): Only return victims that are equal or younger than this age
        ethnicity(Optional, default: all ethnicity): Only return victims that are of the specified ethnicities 
        armed(Optional, default: all): Only return victims that were specified to be armed or not

    RESPONSE: Returns a list of JSON, which of each are victims met the specified paramters, if there are any. 
        date - (date) The date of the shooting 
        name - (String) The name of the victim
        age - (Integer) The age of the victim 
        gender - (String) The gender of the victim
        ethnicity - (String) The ethnicity of victim 
        armed - (String) An armed or unarmed indicator

    Example: 
        http://.../victims?state=Alaska&max_year=2003&armed=unarmed
    """
    pass

app.route('/victims/analyze/year/<state>')
def get_years_vis_data(state):
    pass

app.route('/victims/analyze/ethnicity/<state>')
def get_ethnicity_vis_data(state):
    pass

app.route('/victims/analyze/armed/<state>')
def get_armed_vis_data(state):
    pass

app.route('/victims/analyze/gender/<state>'):
def get_gender_vis_data(state):
    pass 



