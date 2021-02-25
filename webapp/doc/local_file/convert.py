import csv 

def create_state():
    """
        1. Open shootings.csv
        2. Open 'states.csv'
        3. Write into 'states.csv'
    """
    kaggle_csv = 'shootings.csv'
    state_csv = 'states.csv'
    state_list = []
    

    with open(kaggle_csv, mode = 'r') as kaggle_file:
        csv_file = csv.reader(kaggle_file)

        with open(state_csv, mode = 'w') as state_file:
            state_writer = csv.writer(state_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            state_id = 0 

            for csv_row in csv_file:
                if csv_row[9] not in state_list and csv_row[0] != 'id':
                    state_list.append(csv_row[9])

            state_list.sort() 
            
            for states in state_list:
                state_writer.writerow([state_id, states])
                state_id += 1
            
            state_writer.writerow([state_id, 'ALL'])


def create_victims():
    kaggle_csv = 'shootings.csv'
    victims_csv = 'victims.csv'
    victim_id = 0

    with open(kaggle_csv, mode = 'r') as kaggle_file:
        csv_file = csv.reader(kaggle_file)

        with open(victims_csv, mode = 'w') as victims_file:
            victims_writer = csv.writer(victims_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for csv_row in csv_file:
                if csv_row[0] != 'id':
                    victims_writer.writerow([victim_id, csv_row[1], csv_row[7], csv_row[5], csv_row[2], csv_row[4], csv_row[6]])
                    victim_id += 1

def create_victim_state():
    kaggle_csv = 'shootings.csv'
    states_csv = 'states.csv'
    victims_csv = 'victims.csv'
    victim_state = 'victim_state.csv'

    state_dict = {}
    victim_dict = {}

    with open(kaggle_csv, mode = 'r') as kaggle_file:
        kaggle_reader = csv.reader(kaggle_file)

        with open(victims_csv, mode = 'r') as victims_file:
            victims_reader = csv.reader(victims_file)

            with open(states_csv, mode = 'r') as states_file:
                states_reader = csv.reader(states_file)

                with open(victim_state, mode = 'w') as victim_state_file:
                    victim_state_writer = csv.writer(victim_state_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    for state_row in states_reader:
                        state_dict[state_row[1]] = state_row[0]
                    
                    for victim_row in victims_reader:
                        victim_dict[victim_row[1]] = victim_row[0]
                    
                    for kaggle_row in kaggle_reader:
                        if kaggle_row[0] != 'id':
                            victim_state_writer.writerow([victim_dict[kaggle_row[1]], state_dict[kaggle_row[9]]])
                    

                    

                

def main():
    #convert_id()
    create_state()
    create_victims()
    create_victim_state()

if __name__ == "__main__":
    main()