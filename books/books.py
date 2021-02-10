'''
Author: Tianyi Lu, Victor Huang
Revised by: Victor Huang
Description: Gets arguments from users and then searchs for books matching user argument input
Date: 2021-01-15 09:10:29
LastEditors: Tianyi Lu
LastEditTime: 2021-01-15 16:12:59

REVISION SUMMARY:
Revised some function names to match the purpose of said functions better. Changed some variable
names following the "snake case" preference detailed in the Style Guide for Python Code. Made sure
functions served a singular purpose simply and effectively. Added some comments to make understanding
code easier. Followed the Style Guide as much as possible.
'''

import argparse
import csv

# Creats a book
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

# This function only gets arguments from the user
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

# This function only loads the files from the books.csv file
def load_books():
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

def get_books_by_title(args, books):
    """
    Get books whose titles contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A list of book objects whose title matches the arguments.
    """
    if not args.title:
        return None

    title_list = []
    for arg in args.title:
        for book in books:
            if arg.lower() in book.title.lower():
                if not book in title_list:
                    title_list.append(book)
    return title_list              
        
# This function only serves the purpose of getting books 
def get_books_by_author(args, books):
    """
    Get books whose author name contains the arguments
    :param args: args object containing all arguments
    :param books: A list of book objects read from csv file
    :return: A dictionary with matched authors' names as key and a list of their
             book objects as value.
    """
    if not args.author:
        return None

    author_dictionary = {}
    # Create a key value pair for every author that matches the arguments
    for arg in args.author:
        for book in books:
            if arg.lower() in book.author.lower():
                if not book.author in author_dictionary.keys():
                    author_dictionary[book.author] = []

    # Fill in the books written by every author in the dictionary
    for book in books:
        if book.author in author_dictionary.keys():
            author_dictionary[book.author].append(book)

    
    return author_dictionary

def get_books_by_year(args, books):
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
    year_list = []
    sortedYears = sorted(args.year)
    while i < (len(args.year) - 1):
        for book in books:
            if int(book.year) >= sortedYears[i] and int(book.year) <= sortedYears[i + 1]:
                if not book in year_list:
                    year_list.append(book)
        i += 2

    return year_list

# This function only serves the purpose of finding the repeated values in the two lists
def intersection(lst1, lst2):
    """
    Find the intersection of two lists
    :param lst1: List One
    :param lst2: List Two
    :return: A list of intersect elements in the two lists
    """
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

# This function only serves the purpose of combing all the results
def combine(title_list, author_dictionary, year_list):
    """
    Combine the results from get_books_by_title, get_books_by_year, and get_books_by_author. Print out the
    formated results
    :param title_list: A list of book objects from get_books_by_title
    :param author_dictionary: A dictionary of author and book objects from get_books_by_author
    :param year_list: A list of book objects from get_books_by_year
    """
    # Intersection list of title_list and year_list
    title_year_list = []

    only_author_dictionary = False

    # If both title and year arguments appeared in the command line input
    if (title_list is not None) and (year_list is not None):
        title_year_list = intersection(title_list, year_list)

    # If only the title argument appeared in the command line input
    elif title_list:
        title_year_list = title_list

    # If only the year argument appeared in the command line input
    elif year_list:
        title_year_list = year_list

    # If only the author argument appeared in the command line input
    else:
        only_author_dictionary = True

    if author_dictionary:
        for author, books in author_dictionary.items():
            if not only_author_dictionary:
                author_dictionary[author] = intersection(books, title_year_list)
        for author in author_dictionary.keys():
            print()
            print(author+": ")
            if not author_dictionary[author]:
                print( "\t(No book matches)")
            else:
                for book in author_dictionary[author]:
                    print("\t" + str(book))
                
    else:
        print("\n%d books found\n" % len(title_year_list))
        for i, book in enumerate(title_year_list):
            print(str(i+1)+". "+str(book))

if __name__ == "__main__":
    args = get_arguments()
    books = load_books()
    title_list = get_books_by_title(args, books)
    year_list = get_books_by_year(args, books)
    author_dictionary = get_books_by_author(args, books)
    combine(title_list, author_dictionary, year_list)
    
