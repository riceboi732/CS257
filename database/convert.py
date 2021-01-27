#author: Victor Huang, Silas Zhao

import csv 
def openfile(filename):
    csvFile =open(filename, "r")
    reader = csv.reader(csvFile)
    return reader

def writefile(reader,olympians, sports_and_events, olympics,olympians_olympics,sports_events_and_olympians):
    # table1 olympians:

    #table1:
    csvFile1 = open(olympians, "w")
    olympians_w= csv.writer(csvFile1)

    #table2:
    csvFile2 = open(sports_and_events, "w")
    sports_and_events_w = csv.writer(csvFile2)

    #table3:
    csvFile3 = open(olympics, "w")
    olympics_w = csv.writer(csvFile3)
    
    #table4: linked table
    csvFile4 = open(olympians_olympics, "w")
    olympians_olympics_w = csv.writer(csvFile4)

    csvFile5 = open(sports_events_and_olympians, "w")
    sports_events_and_olympians_w = csv.writer(csvFile5)

    #check redundancy
    olympics_set = []
    olympians_set = []
    olympians_olympics_set = []
    sports_and_events_set = []
    sports_events_and_olympians_set = []
    for row in reader:
        olympians = []
        olympics = []
        sports_and_events = []
        olympians_olympics = []
        sports_events_and_olympians = []
        if reader.line_num == 1:
            continue
        for i in range(len(row)):
            if in_olympians(i):
                olympians.append(row[i])
            elif in_olympics(i):
                olympics.append(row[i])
            else:
                sports_and_events.append(row[i])
        olympians_olympics.append(row[1])
        olympians_olympics.append(row[8])
        sports_events_and_olympians.append(row[1])
        sports_events_and_olympians.append(row[13])
        if sports_and_events not in sports_and_events_set:
            sports_and_events_set.append(sports_and_events)
            sports_and_events_w.writerow(sports_and_events)

        if  olympians_olympics not in olympians_olympics_set:
            olympians_olympics_set.append(olympians_olympics)
            olympians_olympics_w.writerow(olympians_olympics)

        if  olympics not in olympics_set:
            olympics_set.append(olympics)
            olympics_w.writerow(olympics)

        if olympians not in olympians_set:
            olympians_set.append(olympians)
            olympians_w.writerow(olympians)
        
        if sports_events_and_olympians not in sports_events_and_olympians_set:
            sports_events_and_olympians_set.append(sports_events_and_olympians)
            sports_events_and_olympians_w.writerow(sports_events_and_olympians)

def in_olympians(index):
    if index <= 7 or index == 14:
        return True
    else:
        return False

def in_olympics(index):
    if index > 7 and index <= 11:
        return True
    else:
        return False


def main():
    reader = openfile("athlete_events.csv")
    writefile(reader,"olympians.csv", "sports_and_events.csv", "olympics.csv","olympians_olympics.csv","sports_events_and_olympians.csv")
main()
