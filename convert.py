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
    olympics_set = set()
    olympians_set = set()
    olympians_olympics_set = set()
    sports_and_events_set = set()
    sports_events_and_olympians_set = set()
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
        sports_and_events_str = to_String(sports_and_events)
        if sports_and_events_str not in sports_and_events_set:
            sports_and_events_set.add(sports_and_events_str)
            sports_and_events_w.writerow(sports_and_events)
        olympians_olympics_str = to_String(olympians_olympics)
        if  olympians_olympics_str not in olympians_olympics_set:
            olympians_olympics_set.add(olympians_olympics_str)
            olympians_olympics_w.writerow(olympians_olympics)

        olympics_str = to_String(olympics)
        if  olympics_str not in olympics_set:
            olympics_set.add(olympics_str)
            olympics_w.writerow(olympics)
        olympians_str = to_String(olympians)
        if olympians_str not in olympians_set:
            olympians_set.add(olympians_str)
            olympians_w.writerow(olympians)
        sports_events_and_olympians_str = to_String(sports_events_and_olympians)
        if sports_events_and_olympians_str not in sports_events_and_olympians_set:
            sports_events_and_olympians_set.add(sports_events_and_olympians_str)
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

def to_String(list):
    s = ""
    for i in range(len(list)):
        s += list[i]
        s += " "
    return s

def main():
    reader = openfile("athlete_events.csv")
    writefile(reader,"olympians.csv", "sports_and_events.csv", "olympics.csv","olympians_olympics.csv","sports_events_and_olympians.csv")
main()
