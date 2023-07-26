from flask import Flask,render_template,redirect,url_for,request
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/bookList')
def bookList():
    books=database.bookList()

    print(books)
    return render_template("bookList.html",books=books)

@app.route('/addBook',methods=["GET","POST"])
def addBook():
     if(request.method=='POST'):
        name=request.form['name']
        author=request.form['author']
        id=request.form['id']
        copies=author=request.form['copies']

        mssg=database.addBook(name,author,copies,id)
       
        return render_template("addBook.html",mssg=mssg)
     return render_template("addBook.html")


@app.route('/addUser',methods=["GET","POST"])
def addUser():
     if(request.method=='POST'):
        name=request.form['name']
        email=request.form['email']
        errorMsg=database.verifyUser(name,email)
        
        return render_template("addUser.html",errorMsg=errorMsg)
        
     return render_template("addUser.html")

@app.route('/issueBook',methods=["GET","POST"])
def issueBook():
    if(request.method=='POST'):
        id=request.form['id']
        email=request.form['email']
        mssg=database.issueBook(id,email)
        ##mssg="hi"
        return render_template("issueBook.html",mssg=mssg)
    return render_template("issueBook.html")

@app.route('/returnBook',methods=["GET","POST"])
def returnBook():
    if(request.method=='POST'):
        id=request.form['id']
        email=request.form['email']
        mssg=database.returnBook(id,email)
        return render_template("returnBook.html",mssg=mssg)
    return render_template("returnBook.html")

@app.route("/issueList")
def issueList():
    issues=database.issueList()
    return render_template("issueList.html",issues=issues)


@app.route("/payFine",methods=["GET","POST"])
def payFine():
    
    if(request.method=="POST"):
        try:
            email=request.form['email']
            fine=database.getFine(email)
            if(fine=="0"):
                fine="Fine does not exist"
                return render_template("payFine.html",mssg=fine)
            return render_template("payment.html",fine=fine,email=email)
        except:
            email = request.form.get('clicked_button_id')
            database.payFine(email)
            return render_template("payFine.html",mssg="Fine Successfully Paid")
        
    return render_template("payFine.html")

if __name__ == '__main__':

    app.run()