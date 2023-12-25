import mysql.connector as sql
import requests as r
import json
from datetime import datetime as dt
from prettytable import PrettyTable

db = sql.connect(
  host = "localhost",
  user = "root",
  password = "1234",
  database = 'project',
	)
cursor = db.cursor()

def get_book(isbn):
  url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{str(isbn)}'
  book_req= r.get(url)# Getting Data from Google Books API
  book_json = book_req.json() #Converting  Requests data to Dict
  book = book_json['items'][0]['volumeInfo'] #Extracting data of  1st book
  #print(book)
  data = {}
  data['isbn'] = str(isbn)
  data['name'] = (book['title']).replace("'", "")
  data['author'] = (book['authors'][0])
  data['rating'] = (book['averageRating'])*2*10
  return data

def add_book(isbn):
	try:
		book = get_book(isbn)
		cursor.execute(f"insert into books values('{book['isbn']}', '{book['name']}', '{book['author']}', {book['rating']});")
		db.commit()
		print(f"{book['name']} is Added!")
	except Exception:
		print("Book Already Exists in the Library!")

def remove_book(isbn):
  try:
    book = get_book(isbn)
    cursor.execute(f"delete from books where isbn='{book['isbn']}';")
    db.commit()
    print(f"{book['name']} is Removed from the Library!")
  except Exception:
    print("Book doesn't exist in the Library!")

def add_member(mid, name, email, phone):
  joining_date = (str(dt.today().year) + "-" +str(dt.today().month) + "-" + str(dt.today().day))
  cursor.execute(f"insert into members values('{mid}', '{name}', '{email}', '{phone}', '{joining_date}');")
  db.commit()
  print(f"'{name}' successfully registered in Database!")

def remove_member(mid):
  cursor.execute(f"delete from members where member_id = '{mid}';")
  db.commit()
  print(f"'{mid}' successfully removed from the Database!")
def lookup(term, field, table):
  cursor.execute(f"select * from {table} where {field}='{term}';")
  if (cursor.fetchone())==None:
    return False
  else:
    return True
def issue_book(mid, isbn):
  issue_date = (str(dt.today().year) + "-" +str(dt.today().month) + "-" + str(dt.today().day))
  cursor.execute(f"insert into records values('{mid}', '{isbn}', '{issue_date}', Null);")
  db.commit()
  print(f"'Book successfully issued!")


def return_book(mid, isbn):
  return_date = (str(dt.today().year) + "-" +str(dt.today().month) + "-" + str(dt.today().day))
  cursor.execute(f"update records set return_date = '{return_date}' where isbn = '{isbn}' and member_id='{mid}';")
  db.commit()
  print(f"'Book successfully returned!")


def startup():
  print('█╗░░░░░██╗██████╗░██████╗░░█████╗░██████╗░██╗░░░██╗')
  print('█║░░░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝')
  print('█║░░░░░██║██████╦╝██████╔╝███████║██████╔╝░╚████╔╝░')
  print('█║░░░░░██║██╔══██╗██╔══██╗██╔══██║██╔══██╗░░╚██╔╝░░')
  print('██████╗██║██████╦╝██║░░██║██║░░██║██║░░██║░░░██║░░░')
  print('══════╝╚═╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░')
  print("Welcome to Books Management System!")
  print("Select an Option:")
  print(" ➤  1 | Add a Book to Library")
  print(" ➤  2 | Remove a Book from Library")
  print(" ➤  3 | View Book Database")
  print(" ➤  4 | Search a Book in Database")
  print(" ➤  5 | Add a Member")
  print(" ➤  6 | Remove a Member")
  print(" ➤  7 | Issue a Book")
  print(" ➤  8 | Return a Book")
  print(" ➤  9 | View Members")
  print(" ➤ 10 | View Book Status")
  print(" ➤ 11 | Check Pending Returns")
  choice = int(input("Enter Option Number: "))

  if choice==1:
    isbn = int(input("Enter ISBN Number of the Book you wish to Add: "))
    add_book(isbn)

  elif choice==2:
    isbn = int(input("Enter ISBN Number of the Book you wish to Remove: "))
    remove_book(isbn)

  elif choice==3:
    print("\nHow you want to retrieve the database?")
    print(" ➤ 1 | Alphabatical Order")
    print(" ➤ 2 | Alphabatical Order (Descending)")
    print(" ➤ 3 | Rating Wise")
    print(" ➤ 4 | Rating Wise (Descending)")
    order_choice = int(input("Enter the Option Number: "))
    if order_choice==1:
      cursor.execute(f"select * from books order by name")
      books = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['ISBN', 'Name', 'Author', 'Rating']
      for book in books:
        stars = (int(int(book[3])/10) * "★") + (int(10 - int(int(book[3])/10)) * "☆")
        table.add_row([book[0], book[1], book[2], stars])
      print(table)
    elif order_choice==2:
      cursor.execute(f"select * from books order by name desc")
      books = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['ISBN', 'Name', 'Author', 'Rating']
      for book in books:
        stars = (int(int(book[3])/10) * "★") + (int(10 - int(int(book[3])/10)) * "☆")
        table.add_row([book[0], book[1], book[2], stars])
      print(table)

    elif order_choice==3:
      cursor.execute(f"select * from books order by rating")
      books = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['ISBN', 'Name', 'Author', 'Rating']
      for book in books:
        stars = (int(int(book[3])/10) * "★") + (int(10 - int(int(book[3])/10)) * "☆")
        table.add_row([book[0], book[1], book[2], stars])
      print(table)

    elif order_choice==4:
      cursor.execute(f"select * from books order by rating desc")
      books = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['ISBN', 'Name', 'Author', 'Rating']
      for book in books:
        stars = (int(int(book[3])/10) * "★") + (int(10 - int(int(book[3])/10)) * "☆")
        table.add_row([book[0], book[1], book[2], stars])
      print(table)

  elif choice==4:
    search_choice = (input("What do you want to Search? : "))
    cursor.execute(f"select * from books where name like '%{search_choice}%' or isbn like '%{search_choice}%' or author like '%{search_choice}%';")
    books = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ['ISBN', 'Name', 'Author', 'Rating']
    for book in books:
      stars = (int(int(book[3])/10) * "★") + (int(10 - int(int(book[3])/10)) * "☆")
      table.add_row([book[0], book[1], book[2], stars])
    print(table)


  elif choice==5:
    print("\n<====== ADD MEMBER =====>")
    member_id = "KC/" + str(input("Enter Your Admission number: KC/"))
    name = (input("Enter Your Name: "))
    email = (input("Enter Your Email: "))
    phone = "+91" + (input("Enter Your Phone Number: +91"))
    try:
      add_member(member_id, name, email, phone)
    except Exception as e:
      print(e)
      print('Member already Exists!')


  elif choice==6:
    print("\n<====== REMOVE MEMBER =====>")
    member_id = "KC/" + str(input("Enter Your Admission number of member you wish to remove: KC/"))
    remove_member(member_id)


  elif choice==7:
    print("\n<====== ISSUE BOOK =====>")
    member_id = "KC/" + str(input("Enter Your Admission number: KC/"))
    if not (lookup(member_id, "member_id", 'members')):
      print("Member Doesn't Exist")
    else:
      isbn = str(input("Enter ISBN of the Book you want to issue:"))
      if not (lookup(isbn, "isbn", 'books')):
        print("Books Not Found in Library!")
      else:
        issue_book(member_id, isbn)


  elif choice==8:
    print("\n<====== RETURN BOOK =====>")
    member_id = "KC/" + str(input("Enter Your Admission number: KC/"))
    if not (lookup(member_id, "member_id", 'members')):
      print("Member Doesn't Exist")
    else:
      isbn = str(input("Enter ISBN of the Book you want to return:"))
      if not (lookup(isbn, "isbn", 'records')):
        print("Book Not Issued Yet!")
      else:
        return_book(member_id, isbn)

  elif choice==9:
      cursor.execute(f"select * from members")
      members = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['Member ID', 'Name', 'E-mail', 'Phone', "Date Joined"]
      for member in members:
        table.add_row([member[0], member[1], member[2], member[3], member[4]])
      print(table)
  elif choice==10:
      cursor.execute(f"select r.member_id, m.name, b.name, r.isbn, r.issue_date, r.return_date from records r, members m, books b where r.isbn=b.isbn;")
      members = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['Member ID', 'Name', 'Book Name', 'ISBN', 'Issue Date', 'Return Date']
      for member in members:
        if member[5]==None:
          table.add_row([member[0], member[1], member[2], member[3], member[4], 'PENDING!'])
        else:
          table.add_row([member[0], member[1], member[2], member[3], member[4], member[5]])
      print(table)

  elif choice==11:
      cursor.execute(f"select r.member_id, m.name, b.name, r.isbn, r.issue_date, r.return_date from records r, members m, books b where r.isbn=b.isbn and return_date is null;")
      members = cursor.fetchall()
      table = PrettyTable()
      table.field_names = ['Member ID', 'Name', 'Book Name', 'ISBN', 'Issue Date']
      for member in members:
        table.add_row([member[0], member[1], member[2], member[3], member[4]])
      print(table)

startup()
