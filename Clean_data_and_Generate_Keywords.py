import csv
import os
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer 
from nltk.tokenize import sent_tokenize, word_tokenize 

print("Begin the Clean_data_and_Generate_Keywords\n")


class user_class:
  def __init__(self, User_ID, Location,Age):
    self.User_ID = int(User_ID)
    self.Location = Location
    self.Age = Age

  def print(self):
    print("User_ID :",self.User_ID)
    print("Location :",self.Location)
    print("Age :",self.Age)

class final_book:
  def __init__(self, ISBN, Book_Title,Keywords,Book_Author,Publisher):
    self.ISBN = ISBN
    self.Book_Title = Book_Title
    self.Book_Author = Book_Author
    self.Publisher = Publisher  
    self.Keywords = Keywords  

  def print(self):
    print("ISBN :",self.ISBN)
    print("Book_Title :",self.Book_Title)
    print("Book_Author :",self.Book_Author)
    print("Publisher :",self.Publisher)
    print("Keywords :",self.Keywords)


class book_class:
  def __init__(self, ISBN, Book_Title,Book_Author,Publisher):
    self.ISBN = ISBN
    self.Book_Title = Book_Title
    self.Book_Author = Book_Author
    self.Publisher = Publisher  

  def print(self):
    print("ISBN :",self.ISBN)
    print("Book_Title :",self.Book_Title)
    print("Book_Author :",self.Book_Author)
    print("Publisher :",self.Publisher)

class rate_class:
  def __init__(self, User_ID, ISBN,Book_Rating):
    self.User_ID = int(User_ID)
    self.ISBN = ISBN
    self.Book_Rating = Book_Rating

  def print(self):
    print("User_ID :",self.User_ID)
    print("ISBN :",self.ISBN)
    print("Book_Rating :",self.Book_Rating)


def Read_users(List_1):
    with open("BX-Users.csv","r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        next(csv_reader)
        for x in csv_reader:
            item = user_class(x[0],x[1],x[2])
            List_1.append(item)
def Read_books(List_1):
    with open("BX-Books.csv","r",encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        next(csv_reader)
        for x in csv_reader:
           # print(x[0],x[1],x[2],x[3])
            item = book_class(x[0],x[1],x[2],x[3])
            List_1.append(item)
def Read_rates(List_1):
    with open("BX-Book-Ratings.csv","r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        next(csv_reader)
        for x in csv_reader:
            item = rate_class(x[0],x[1],x[2])
            List_1.append(item)

def Write_To_Cvs_User(file_name,list1):
    with open(file_name+".csv","w",newline='') as new_file:
        csv_write = csv.writer(new_file, delimiter=';')
        for x in list1:
            csv_write.writerow([str(x.User_ID),str(x.Location),str(x.Age)])

def Write_To_Cvs_Book(file_name,list1):
    with open(file_name+".csv","w",newline='',encoding="utf-8") as new_file:
        csv_write = csv.writer(new_file, delimiter=';')
        for x in list1:
            csv_write.writerow([str(x.ISBN),str(x.Book_Title),str(x.Keywords),str(x.Book_Author),str(x.Publisher)])

def Write_To_Cvs_Rate(file_name,list1):
    with open(file_name+".csv","w",newline='') as new_file:
        csv_write = csv.writer(new_file, delimiter=';')
        for x in list1:
            rawRow = []
            rawRow.append(str(x.User_ID)) #Appending Date
            rawRow.append(str(x.ISBN))   #Appending data
            rawRow.append(str(x.Book_Rating)) 
            csv_write.writerow(rawRow)

def check_in_list_User(value,times,start):
    ara = []
    count = 0
    flag = True
    while flag and start<len(list_of_rates):
        if int(list_of_rates[start].User_ID)>int(value):
            flag = False
            start -= 1
        elif int(list_of_rates[start].User_ID)==int(value):
            count+=1
        start += 1
    ara.append(start)
    if count>=times:
        ara.append(1)
        return ara
    else:
        ara.append(0)
        return ara

def check_in_Books(value,times,start):
    ara = []
    count = 0
    flag = True
    while flag and start<len(list_of_rates):
        if str(value)<str(list_of_rates[start].ISBN):
            flag = False
            start -= 1
        elif str(list_of_rates[start].ISBN)==str(value):
            count+=1
        start += 1    
    ara.append(start)
    if count>=times:        
        ara.append(1)
        return ara
    else:
        ara.append(0)
        return ara

def Clean_Users():
    temp_list_of_users = []
    user_pointer = 0
    list_of_rates.sort(key=lambda x: x.User_ID)
    list_of_users.sort(key=lambda x: x.User_ID)
    for i in range(0,len(list_of_users)):
        v = check_in_list_User(list_of_users[i].User_ID,5,user_pointer)
        user_pointer = int(v[0])
        if v[1]==1:
            temp_list_of_users.append(list_of_users[i])
    print("New size of Users :",len(temp_list_of_users))
    Write_To_Cvs_User("BX-Users-New",temp_list_of_users)
    
def Clean_Books():
    temp_list_of_books=[]
    book_pointer =0
    list_of_books.sort(key=lambda x: x.ISBN)
    list_of_rates.sort(key=lambda x: x.ISBN)
    for i in range(0,len(list_of_books)):
        v = check_in_Books(list_of_books[i].ISBN,10,book_pointer)
        book_pointer = int(v[0])
        if v[1]==1:
            cur_book = final_book(list_of_books[i].ISBN,list_of_books[i].Book_Title,
            generate_keywords(list_of_books[i].Book_Title),list_of_books[i].Book_Author,list_of_books[i].Publisher)
            temp_list_of_books.append(cur_book)
    print("New size of Books :",len(temp_list_of_books))
    Write_To_Cvs_Book("BX-Books-New",temp_list_of_books)

def generate_keywords(word):
    word = word.replace("\\", "")
    word = word.replace("''", " ")
    #print("word",word)
    word = word.lower()
    for char in word:
        if char in "?.!/;:-+()''":
            word = word.replace(char,'')
    #print(word)
    word = word.replace('"',' ')
    #print("after ->  ",word)
    example_sent = word

    stop_words = set(stopwords.words('english')) 
    #print (stop_words)
    word_tokens = word_tokenize(example_sent) 
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
    filtered_sentence = [] 
    
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
   # print("word_tokens") 
    
   # print(word_tokens) 

   # print("stop_words") 

   # print(filtered_sentence)

    p = [',','.','!',"-","=","+","?","/","\\","'","~"]
    removeSymols = [w for w in filtered_sentence if not w in p] 
   # print("removeSymols") 
   # print(removeSymols) 


    #print("Stemming") 
    ps = PorterStemmer() 
    
    # choose some words to be stemmed 
    Stemming = []
    for w in removeSymols: 
        Stemming.append( ps.stem(w))
    #print(Stemming) 

    Stemming = list(dict.fromkeys(Stemming))
   # print("Duplicate") 
   # print(Stemming) 
    teliko = ','.join([str(elem) for elem in Stemming])
    #print(teliko,"\n")
    return teliko


list_of_users = []
list_of_books = []
list_of_rates = []

Read_users(list_of_users)
Read_books(list_of_books)
Read_rates(list_of_rates)





print("list_of_users : "+ str(len(list_of_users)))        
print("list_of_books : "+ str(len(list_of_books)))        
print("list_of_rates : "+ str(len(list_of_rates)))        
print("\n")

Clean_Users()
Clean_Books()

os.system('pause')