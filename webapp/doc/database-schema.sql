CREATE TABLE states(
	id int,
	state_name text
);


CREATE TABLE victims(
	id int,
	victim_name text, 
	victim_ethnicity text, 
	victim_age float, 
	incident_date date, 
	armed_status text, 
	victim_gender text 
);

CREATE TABLE victim_state(
	victim_id int,
	state_id int
)
