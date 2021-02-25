state = 'all'
min_year = '1000'
max_year = 5000
min_age = -10000
max_age = 10000
ethnicity = 'all'
armed = 'all'

state_check = '%' + state + '%'
min_year_check = min_year
max_year_check = max_year
min_age_check = min_age 
max_age_check =  max_age 
ethnicity_check = '%' + ethnicity + '%'
armed_check = '%' + armed + '%'

check = (state_check, min_age_check, max_age_check, ethnicity_check, armed_check, min_year_check, max_year_check, )

query = '''SELECT victims.incident_date, victims.victim_name, 
                victims.victim_age, victims.victim_gender, victims.victim_ethnicity, victims.armed_status, states.state_name 
                FROM victim_state, victims, states 
                WHERE states.state_name = %all% AND victims.id = victim_state.victim_id AND states.id = victim_state.state_id 
                AND victims.victim_age >= %-10000% AND victims.victim_age <= 10000
                AND victims.victim_ethnicity = %'all'%
                AND victims.armed_status = %s 
                AND victims.incident_date BETWEEN '01-01-%i' AND '12-31-%i' 
                ORDER BY victims.incident_date;''' 
test = "2005' OR 1=1;--"

test_check = '%' + test + '%'


print(test_check)