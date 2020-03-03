import csv
import random
import os
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer 
from nltk.tokenize import sent_tokenize, word_tokenize 

print("Begin the Recommended_system \n")

class Sort_Item:
    def __init__(self, book, count,value):
        self.book = book
        self.count = count
        self.value = value

class GloBalBook:
    def __init__(self, book, rate):
        self.book = book
        self.rate = rate

    def printGlob(self):
        self.book.print()
        print("Rate : ",self.rate)

class Book:
  def __init__(self, User_keywords, User_authors,User_years,isbn):
    self.User_keywords = User_keywords
    self.User_authors = User_authors
    self.User_years = User_years
    self.isbn = isbn
    
  def print(self):
    print("Keywords :",self.User_keywords)
    print("Authors :",self.User_authors)
    print("Years :",self.User_years)

class user_class:
  def __init__(self, User_ID, Location,Age):
    self.User_ID = User_ID
    self.Location = Location
    self.Age = Age

  def print(self):
    print("User_ID :",self.User_ID)
    print("Location :",self.Location)
    print("Age :",self.Age)

class book_class:
  def __init__(self, ISBN, Book_Title,Keywords,Book_Author,Publisher):
    self.ISBN = ISBN
    self.Book_Title = Book_Title
    self.Keywords = Keywords
    self.Book_Author = Book_Author
    self.Publisher = Publisher

  def print(self):
    print("ISBN :",self.ISBN)
    print("Book_Title :",self.Book_Title)
    print("Keywords :",self.Keywords)
    print("Book_Author :",self.Book_Author)
    print("Publisher :",self.Publisher)

class rate_class:
  def __init__(self, User_ID, ISBN,Book_Rating):
    self.User_ID = User_ID
    self.ISBN = ISBN
    self.Book_Rating = Book_Rating

  def print(self):
    print("User_ID :",self.User_ID)
    print("ISBN :",self.ISBN)
    print("Book_Rating :",self.Book_Rating)

class Final_Book:
  def __init__(self, book, value):
    self.book = book
    self.value = value

def Read_Users(List_1):
    with open("BX-Users-New.csv","r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for x in csv_reader:
            item = user_class(x[0],x[1],x[2])
            List_1.append(item)

def Read_Books(List_1):
    with open("BX-Books-New.csv","r",encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for x in csv_reader:
            item = book_class(x[0],x[1],x[2],x[3],x[4])
            List_1.append(item)

def Read_Rates(List_1):
    with open("BX-Book-Ratings.csv","r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        for x in csv_reader:
            item = rate_class(x[0],x[1],x[2])
            List_1.append(item)
            
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  

def CheckInTableBooks(value):
    for item in list_of_books:
        if item.ISBN == value:
            return 1
    return 0

def CheckInTableRates(value,user_id):
    for item in list_of_rates:
        if item.ISBN == value and item.User_ID==user_id:
            return 0
    return 1

def GetBookWithISBN(isbn):
    for item in list_of_books:
        if item.ISBN == isbn:
            #print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
            #print(type(item.Keywords))
           # print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")

            return item

def Get_User_Books(user_id):
   # print("user_id",user_id)
    user_books = []
    for item in list_of_rates:
        if item.User_ID==user_id and CheckInTableBooks(item.ISBN) == 1 :
            current = GloBalBook(GetBookWithISBN(item.ISBN),item.Book_Rating)
            user_books.append(current)
            #print(item.ISBN)
    return user_books

def Check_Book_User_Dont_Rate(book_isbn,user_id,start):
    ara = []
    flag = True
    count = 0
    while flag and start<len(list_of_rates):
        if str(list_of_rates[start].ISBN)>str(book_isbn):
            flag = False
            start -= 1
        elif str(list_of_rates[start].ISBN)!=str(book_isbn) and list_of_rates[start].User_ID!=user_id:
            count=1
        start += 1    
    ara.append(start)
    ara.append(count)
    return ara

def Book_filtering(User):
    User.User_authors=User.User_authors.split(",")
    User.User_years=User.User_years.split(",")
    User.User_keywords=User.User_keywords.split(",")
    User.User_keywords = list(dict.fromkeys(User.User_keywords))

def dice_coefficient(a, b):
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0/(len(a_bigrams) + len(b_bigrams))

def Get_Book_User_Dont_Rate(user_id):
    book_pointer = 0
    temp_list = []
    list_of_books.sort(key=lambda x: x.ISBN)
    list_of_rates.sort(key=lambda x: x.ISBN)
    
    for i in range(0,len(list_of_books)):
        v = Check_Book_User_Dont_Rate(list_of_books[i].ISBN,user_id,book_pointer)
        book_pointer = int(v[0])
        if(v[1]==1):
            temp_list.append(list_of_books[i])
    
    #print("All :",len(list_of_books),"Dont Rate: ",len(temp_list))
    return temp_list

def WithJaccard(b1_keyword,b1_author,b1_year,b2_keyword,b2_author,b2_year):
    jaccard = jaccard_similarity(b1_keyword,b2_keyword)*0.2
    author = 0
    year = 0
    if b2_author[0] in b1_author :
         author=0.4
    min = 5000
    for y in b1_year:
        current_year = abs(int(y)-int(b2_year[0]))
        if(current_year<min):
            min = current_year
    year = (1-((min)/2005))*0.4
    final = jaccard+author+year
    return final

def With_dice_coefficient(b1_keyword,b1_author,b1_year,b2_keyword,b2_author,b2_year):
    dice = dice_coefficient(b1_keyword,b2_keyword)*0.5
    author = 0
    year = 0
    #print ("b1_year :",b1_year)
    if b2_author[0] in b1_author :
         author=0.3
    min = 5000
    for y in b1_year:
        if b1_year=='' or b1_year== " ":
            b1_year = "0"
        current_year = abs(int(y)-int(b2_year[0]))
        if(current_year<min):
            min = current_year
    #print (min)
    year = (1-((min)/2005))*0.2
    final = dice+author+year
    return final

def final_stage (user_book,current_book):
    #print("========================final_stage========================")
    current_book.Keywords = listToString(current_book.Keywords)
    current_book.Book_Author= listToString(current_book.Book_Author)
    current_book.Publisher=listToString(current_book.Publisher)
    current_book.Keywords=current_book.Keywords.split(",")
    current_book.Book_Author=current_book.Book_Author.split(",")
    current_book.Publisher = str(current_book.Publisher)
    current_book.Publisher=current_book.Publisher.split(",")
    
    j = WithJaccard(user_book.User_keywords,user_book.User_authors,user_book.User_years,current_book.Keywords,current_book.Book_Author,current_book.Publisher)
    d = With_dice_coefficient(user_book.User_keywords,user_book.User_authors,user_book.User_years,current_book.Keywords,current_book.Book_Author,current_book.Publisher)
    j = round(j,4)
    d = round(d,4)
    m = Final_Book(current_book,j)
    list_of_Jaccard_books.append(m)
    m = Final_Book(current_book,d)
    list_of_Dice_books.append(m)

def WriteTofile(file,list,type):
    count = 1
    list.sort(key = lambda c: c.value , reverse=True)
    for k in list:
        if(count <=10):
            file.write("\n_________________________________________________________________"+"\n  book isbn: "+k.book.ISBN + "       |        "+type+": "+str(k.value))
        else:
            break
        count+=1

def Check_IF_Exist_inJavard(isbn):
    for item in list_of_Jaccard_books:
        if item.book.ISBN==isbn:
            return 1
    return 0

def Increase_golden_st(isbn):
    for item in golden_standard:
        if item.book.ISBN==isbn:
            item.count+=1

def Overlap(list1,list2):
    list_A = []
    list_B = []
    sum = 0
    for i in range(0, len(list2)):
        list_A.append(list1[i].book.ISBN)
        list_B.append(list2[i].book.ISBN)
        sum += (len(set(list_A).intersection(list_B)))/( len(list_B))
    return sum/(len(list2))


def print_lisst(item_list):
    for item in item_list:
        print(item.book.ISBN, item.value)

list_of_users = []
list_of_books = []
list_of_rates = []
list_of_Jaccard_books = []
list_of_Dice_books=[]

Read_Users(list_of_users)
Read_Books(list_of_books)
Read_Rates(list_of_rates)


# print("list_of_users : "+ str(len(list_of_users)))        
# print("list_of_books : "+ str(len(list_of_books)))        
# print("list_of_rates : "+ str(len(list_of_rates)))        
# print("\n")

#GetRoudpmuser10
random_number = random.sample(range(0, len(list_of_users)), 3)
#random_number = [50]
#print(random_number[0])
for random_item in random_number:
    print("->->->->->->->->->->->->->->->->->->->User<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-")
    current_user_id = list_of_users[random_item].User_ID
    list1_user = Get_User_Books(current_user_id)
    if len(list1_user)!=0:
        list1_user.sort(key=lambda x: x.rate ,reverse=True)
        list1_user = list1_user[:3]
        keywords = ""
        authors = ""
        years = ""
        for item in list1_user:
            keywords+=","+listToString(item.book.Keywords)
            authors+=","+listToString(item.book.Book_Author)
            years+=","+listToString(item.book.Publisher)
        keywords = ''.join(keywords.split(',', 1))    
        authors = ''.join(authors.split(',', 1))    
        years = ''.join(years.split(',', 1)) 
        User_book = Book(keywords ,authors , years,"")
        Book_filtering(User_book)
        print("User_ID : ",current_user_id)
        User_book.print()
        list_of_books_to_check = Get_Book_User_Dont_Rate(current_user_id)
        #=================================================================
        for item in list_of_books_to_check:
            final_stage(User_book,item)
        #=================================================================
        #print("len(list_of_Jaccard_books) :",len(list_of_Jaccard_books))
        #=================================================================
        list_of_Jaccard_books.sort(key=lambda x: x.value, reverse=True)
        list_of_Jaccard_books = list_of_Jaccard_books[:10]
        list_of_Dice_books.sort(key=lambda x: x.value, reverse=True)
        list_of_Dice_books = list_of_Dice_books[:10]
        #=================================================================

        file1 = open("User"+str(current_user_id)+"-Jaccard.txt","w") 
        file2 = open("User"+str(current_user_id)+"-Dice_Coefficient.txt","w")
        WriteTofile(file1,list_of_Jaccard_books,"Jaccard")
        WriteTofile(file2,list_of_Dice_books,"Dice_Coefficient")
        golden_standard = []
        for j_item in list_of_Jaccard_books:
            temp = Sort_Item(j_item.book,1,j_item.value)
            golden_standard.append(temp)
        for d_item in list_of_Dice_books:
            if Check_IF_Exist_inJavard(d_item.book.ISBN) == 1:
                Increase_golden_st(d_item.book.ISBN)
            else:
                temp = Sort_Item(d_item.book,1,d_item.value)
                golden_standard.append(temp)
             
        print("\n")
        golden_standard.sort(key=lambda x: (x.count,x.value), reverse=True)


        print("\nOverlap of Jaccard & Dice coefficient :",Overlap(list_of_Jaccard_books,list_of_Dice_books))
        print("Overlap of Golden standard & Jaccard :",Overlap(golden_standard,list_of_Jaccard_books))
        print("Overlap of Golden standard & Dice coefficient :",Overlap(golden_standard,list_of_Dice_books),"\n")

    else:
        print("The User with ID:",current_user_id,"don't hove books")

os.system('pause')


