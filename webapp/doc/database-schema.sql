CREATE TABLE states(
	id int,
	state_name string
);


CREATE TABLE victims(
	id int,
	victim_name string,
	victim_ethnicity string,
	victim_age int,
	incident_date date,
	armed_status boolean,
	victim_gender string 
);

CREATE TABLE victim_state(
	victim_id int,
	state_id int
)
