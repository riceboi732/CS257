'''
Author: Tianyi Lu, Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 16:12:59
'''

import argparse
import csv

class Book():
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author

    def __repr__(self):
        return ', '.join([self.title, self.year, self.author])
    
    # for 'in' and '==' to work with Book class
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

def get_arguments():
    """
    Get argument from command line
    :return: args object
    """
    parser = argparse.ArgumentParser(prog="python3 books.py",
                                     description='Search books based on different methods.')
    # Accessed by args.title
    parser.add_argument('-t', '--title', type=str, nargs='+',
                        help='print books whose titles contains the argument')
    # Accessed by args.author
    parser.add_argument('-a', '--author', type=str, nargs='+',
                        help='print authors whose names contains the argument and a list of their books')
    # Accessed by args.year
    parser.add_argument('-y', '--year', type=int, nargs='+',
                        help='print books published between two year arguments')                    

    args = parser.parse_args()


    return args

# 
def read_file():
    """
    Load books from books.csv
    :return: A list of book objects
    """
    books = []
    with open('books.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            book = Book(row[0], row[1], row[2])
            books.append(book)
            
    return books

def get_title(args, books):
    """
    Get books whose titles contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects whose title matches the arguments.
    """
    if not args.title:
        return None

    tlist = []
    for arg in args.title:
        for book in books:
            if arg.lower() in book.title.lower():
                if not book in tlist:
                    tlist.append(book)
    return tlist              
        

def get_author(args, books):
    """
    Get books whose author name contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A dictionary with matched authors' names as key and a list of their
             book objects as value.
    """
    if not args.author:
        return None

    adict = {}
    # Create a key value pair for every author that matches the arguments
    for arg in args.author:
        for book in books:
            if arg.lower() in book.author.lower():
                if not book.author in adict.keys():
                    adict[book.author] = []

    # Fill in the books written by every author in the dictionary
    for book in books:
        if book.author in adict.keys():
            adict[book.author].append(book)

    
    return adict

def get_year(args, books):
    """
    Get books published between two year arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects published between two year arguments
    """
    if not args.year:
        return None

    # If an odd number of year arguments are entered, pop out the last one.
    if (len(args.year) % 2) == 1:
        args.year.pop()
        
    i = 0
    ylist = []
    sortedYears = sorted(args.year)
    while i < (len(args.year) - 1):
        for book in books:
            if int(book.year) >= sortedYears[i] and int(book.year) <= sortedYears[i + 1]:
                if not book in ylist:
                    ylist.append(book)
        i += 2

    return ylist
    
def intersection(lst1, lst2):
    """
    Find the intersection of two lists
    :param lst1: List One
    :param lst2: List Two
    :return: A list of intersect elements in the two lists
    """
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def combine(tlist, adict, ylist):
    """
    Combine the results from get_title, get_year, and get_author. Print out the
    formated results
    :param tlist: A list of book objects from get_title
    :param adict: A dictionary of author and book objects from get_author
    :param ylist: A list of book objects from get_year
    """
    # Intersection list of tlist and ylist
    tylist = []

    only_adict = False

    # If both title and year arguments appeared in the command line input
    if (tlist is not None) and (ylist is not None):
        tylist = intersection(tlist, ylist)

    # If only the title argument appeared in the command line input
    elif tlist:
        tylist = tlist

    # If only the year argument appeared in the command line input
    elif ylist:
        tylist = ylist

    # If only the author argument appeared in the command line input
    else:
        only_adict = True

    if adict:
        for author, books in adict.items():
            if not only_adict:
                adict[author] = intersection(books, tylist)
        for author in adict.keys():
            print()
            print(author+": ")
            if not adict[author]:
                print( "\t(No book matches)")
            else:
                for book in adict[author]:
                    print("\t" + str(book))
                
    else:
        print("\n%d books found\n" % len(tylist))
        for i, book in enumerate(tylist):
            print(str(i+1)+". "+str(book))

if __name__ == "__main__":
    args = get_arguments()
    books = read_file()
    tlist = get_title(args, books)
    ylist = get_year(args, books)
    adict = get_author(args, books)
    combine(tlist, adict, ylist)
    
