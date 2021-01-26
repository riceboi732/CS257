import csv 
#converter
#open csv file
#store data to olmpians and olympics
def openfile(filename):
    csvFile =open(filename, "r")
    reader = csv.reader(csvFile)
    return reader

def writefile(reader,filename1, filename2):
    # table1 olympians:

    #table1:
    csvFile1 = open(filename1, "w")
    writer1 = csv.writer(csvFile1)

    #table2:
    csvFile2 = open(filename2, "w")
    writer2 = csv.writer(csvFile2)
    
    #check redundancy
    set1 = []
    set2 = []
    for row in reader:
        d1 = []
        d2 = []
        if reader.line_num == 1:
            continue
        for i in range(len(row)):
            if in_table1(i):
                #if is_int(i):
                #    d1.append(int(row[i]))
                #else:
                d1.append(row[i])
            else:
                #if is_int(i):
                #    d2.append(int(row[i])) 
                #else:
                d2.append(row[i])
        if d1 not in set1:
            set1.append(d1)
            writer1.writerow(d1)
        if d2 not in set2:
            set2.append(d2)
            writer2.writerow(d2)

def in_table1(index):
    if index >=8 and index <=11:
        return False
    elif index == 0:
        return False
    else: 
        return True

def is_int(i):
    if i in [0,3,4,5,9]:
        return True
    return False

def main():
    reader = openfile("athlete_test.csv")
    writefile(reader,"table1.csv","table2.csv")
main()
