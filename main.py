from flask import Flask
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def hello():
    """
    Say hello to the world!

    Returns:
        string: Goooood morning!
    """
    return 'Hello, World!'

#Test of Flask and app.route function
@app.route("/hello/")
def hello2():
    return "Hello 2 the world"

#Test to return json.file
@app.route("/sort/test")
@cross_origin()
def sort_test():
    #Open data.json 
    with open('data.json') as json_data:
        #Tansform .json in a python dictionnary
        json_dic = json.load(json_data)
        json_dic['users'] = sorted(json_dic['users'], key = lambda k: k['name'])
    return json_dic

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------


"""

+-----------+
|           |
|   Users   |
|           |
+-----------+

"""
#Endpoint to sort user by name
@app.route("/users/sort/name")
@cross_origin()
def users_sort_name(): 
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    json_dic['users'] = sorted(json_dic['users'], key = lambda k: k['name'])

    #open a new file.json to have not mistake/loss
    with open('new_data.json','wt') as new_data:
        #Rewrite a specific json file
        new_data.write(json.dumps(json_dic['users'],
                                  indent = 1)) #Display
                                  

    return json_dic



"""

+-----------+
|           |
|   Books   |
|           |
+-----------+

"""

"""

+------+
| Sort |
+------+

"""

#Endpoint to sort books by author
@app.route("/books/sort/author")
@cross_origin()
def books_sort_author(): 
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    json_dic['books'] = sorted(json_dic['books'], key = lambda k: k['author'])

    #open a new file.json to have not mistake/loss
    with open('new_data.json','wt') as new_data:
        #Rewrite a specific json file
        new_data.write(json.dumps(json_dic['books'],
                                  indent = 1)) #Display
                                  

    return json_dic


#Endpoint to sort books by title
@app.route("/books/sort/title")
@cross_origin()
def books_sort_title(): 
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    json_dic['books'] = sorted(json_dic['books'], key = lambda k: k['title'])

    #open a new file.json to have not mistake/loss
    with open('new_data.json','wt') as new_data:
        #Rewrite a specific json file
        new_data.write(json.dumps(json_dic['books'],
                                  indent = 1, #Display
                                  sort_keys = True))
                                  

    return json_dic


"""

+--------+
| Search |
+--------+

"""

#Endpoint to search books by author/title/id
#The third element of the URL is the type of research
#The last element is the research
@app.route("/books/search/type=<string:searchType>&search=<string:name>")
@cross_origin()
def books_search(searchType,name):

    #Remplace '_' by ' '
    #Because space on URL is not correct
    name = name.replace('_',' ')

    #Create new dictionnary for return
    new_dic = {}
    #List of results
    li_results = []
    #Add list on dictionnary
    new_dic["Results"] = li_results
    
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    #If search by author
    if searchType == 'author' or searchType == 'Author':
        for k in json_dic['books']:
            if name == k['author']:
                li_results.append(k)

    #If search by author
    if searchType == 'title' or searchType == 'Title':
        for k in json_dic['books']:
            if name == k['title']:
                li_results.append(k)

    #If search by author
    if searchType == 'id' or searchType == 'Id':
        for k in json_dic['books']:
            if int(name) == k['id']:
                li_results.append(k)

        
    with open('new_data.json','wt') as new_data:
        new_data.write(json.dumps(new_dic,
                                  indent = 1)) #Display
                                  

    return new_dic

"""

+-----------+
|           |
|   Loans   |
|           |
+-----------+

"""

#Endpoint to list all books borrowed by a user
@app.route("/loans/list/borrow/id=<int:id_user>")
@cross_origin()
def borrowed(id_user):

    #Create new dictionnary for return
    new_dic = {}
    #List of results
    li_results = []
    #Add list on dictionnary
    new_dic["Results"] = li_results
    
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    for k in json_dic['loans']:
        if k['id_user'] == id_user:
            #'books' must sort by id
            li_results.append(json_dic['books'][k['id_book']-1])

        
    with open('new_data.json','wt') as new_data:
        new_data.write(json.dumps(new_dic,
                                  indent = 1)) #Display
                                  

    return new_dic

#Endpoint to list loans
@app.route("/loans/list")
@cross_origin()
def list_loans():

    new_dic = {}
    #Lists of results
    li_results_users = []
    li_results_books = []
    
    #Two key in dictionnary
    new_dic["Results_users"] = li_results_users
    new_dic["Results_books"] = li_results_books

    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    for k in json_dic['loans']:
        #Avoid duplicates
        if json_dic['users'][k['id_user']-1] not in li_results_users:
            li_results_users.append(json_dic['users'][k['id_user']-1])

        li_results_books.append(json_dic['books'][k['id_book']-1])

    with open('list_loans.json','wt') as list_loans:
        list_loans.write(json.dumps(new_dic,
                                  indent = 1)) #Display          

    return new_dic

#Endpoint to add or remove loans
@app.route("/loans/<string:operation>/id_user=<int:id_user>&id_book=<int:id_book>")
@cross_origin()
def add_rem_loans(operation,id_user,id_book):
    with open('data.json') as json_data:
        json_dic = json.load(json_data)

    #Refresh loan list (list_loans.json)
    list_loans()
    
    with open('list_loans.json') as json_dic_loans:
        dic_loans = json.load(json_dic_loans)

    #Possible word to use the endpoint (arg of 'operation')
    add = ["add","Add","ADD","+"]
    remove = ["rm","remove","Remove","-"]

    #An dictionnary element
    item = {"id_user":id_user, "id_book":id_book}

    if operation in add:
        #If the book is borrow impossible to add in loans
        #If the user/book are not in data.json : impossible
        if json_dic['books'][id_book-1] not in dic_loans['Results_books'] and id_user <= len(json_dic['users']) and id_book <= len(json_dic['books']):
            json_dic['loans'].append(item)
    
    if operation in remove:
        #Verify if the book is borrow and if the user is a currently borrower
        if json_dic['books'][id_book-1] in dic_loans['Results_books'] and json_dic['users'][id_user-1] in dic_loans['Results_users']:
            json_dic['loans'].remove(item)
            
    with open('data.json','wt') as new_data:
        new_data.write(json.dumps(json_dic,
                                    indent = 1)) #Display          

    return json_dic