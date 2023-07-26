from sqlalchemy import create_engine, Column, String, CHAR,Integer,Date,BOOLEAN,desc,asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import mysql.connector


engine = create_engine('mysql://root:password@localhost/library')

Base = declarative_base()
Base.metadata.bind = engine

class Users(Base):
    __tablename__ = 'users'
    email = Column(String(255), primary_key=True)
    name = Column(String(255))
    fine=Column(Integer)
    numBorrowed=Column(Integer)


class Books(Base):
    __tablename__ = 'bookList'
    name = Column(String(255), primary_key=True)
    id = Column(Integer,primary_key=True)
    author=Column(String(255))
    copies=Column(Integer)
    remainingCopies=Column(Integer)

class Issues(Base):
    __tablename__ = 'issues'
    num=Column(Integer,primary_key=True)
    id = Column(Integer)
    name=Column(String(255))
    email = Column(String(255))
    borrowDate=Column(Date)
    returnDate=Column(Date)
    pending=Column(BOOLEAN,default=True)
    fine=Column(Integer)



Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def issueBook(id,email):
    book=session.query(Books).filter_by(id=id).first()
    user = session.query(Users).filter_by(email=email).first()
    if(not book):
        return "Book does not exist"
    if(not user):
        return "User does not exist"
    if(user.fine>500):
        return "Cannot Borrow,Pending fine must be paid"
    if(user.numBorrowed==3):
        return "Cannot Borrow anymore"
    if(book.remainingCopies==0):
        return "Book not available"
    book.remainingCopies=book.remainingCopies-1
    user.numBorrowed+=1
    session.commit()
    ##add new table and update date and id 
    currDate=datetime.date.today()
    new_issue = Issues(id=id,email=email,name=book.name,borrowDate=currDate,returnDate=None,fine=0,pending=True)
    session.add(new_issue)
    session.commit()
    return "Book Successfully Borrowed"


def returnBook(id,email):
    book=session.query(Books).filter_by(id=id).first()
    user = session.query(Users).filter_by(email=email).first()
    if(not book):
        return "Book does not exist"
    if(not user):
        return "User does not exist"
    ##verify if given book was actually borrowed
    returnData=session.query(Issues).filter_by(id=id,email=email).first()
    if(not returnData):
        return "Given user never borrowed the book"
    if(returnData.pending==False):
        return "Given user has currently not borrowed the book"
    returnData.returnDate=datetime.date.today()
    duration=(returnData.returnDate-returnData.borrowDate).days
    if(duration>7):
        user.fine+=(duration-7)*100
        returnData.fine=user.fine
    book.remainingCopies=book.remainingCopies+1
    user.numBorrowed-=1
    returnData.pending=False
    session.commit()
    ##add new table and update date and id there
    
    return "Book Successfully Returned"
    


def bookList():
    books = session.query(Books).order_by(Books.name).all()
    booksDict = [{'id': book.id, 'name': book.name,'author':book.author,'copies':book.copies,'remainingCopies':book.remainingCopies} for book in books]
    return booksDict

def issueList():
    
    issues = session.query(Issues).order_by(desc(Issues.pending), asc(Issues.borrowDate)).all()
    for issue in issues:
        if(issue.pending):
            duration=(datetime.date.today()-issue.borrowDate).days
            if(duration>7):
                issue.fine=(duration-7)*100
    issuesDict = [{'id': issue.id, 'name': issue.name, 'email': issue.email, 'pending': issue.pending,
                   'borrowDate': issue.borrowDate, 'returnDate': issue.returnDate, 'fine': issue.fine}
                  for issue in issues]
    return issuesDict

def addBook(name,author,copies,id):
    u1 = session.query(Books).filter_by(name=name).first()
    u2=session.query(Books).filter_by(id=id).first()
    if u1:
        return "Book already exists with given name"
    if u2:
        return "Book already exists with given ID"
    new_book = Books(name=name,id=id,author=author,copies=copies,remainingCopies=copies)
    session.add(new_book)
    session.commit()
    return "Book Successfully Added!"
        


def verifyUser(name,email):
    user = session.query(Users).filter_by(email=email).first()
 
    if user:
        return "User already exists"
    new_user = Users(email=email,name=name,fine=0,numBorrowed=0)
    session.add(new_user)
    session.commit()
    return "User Added Successfully"

def getFine(email):
    user=session.query(Users).filter_by(email=email).first()
    if not user:
        return "0"
    return str(user.fine)
def payFine(email):
     user=session.query(Users).filter_by(email=email).first()
     user.fine=0
     session.commit()
     


