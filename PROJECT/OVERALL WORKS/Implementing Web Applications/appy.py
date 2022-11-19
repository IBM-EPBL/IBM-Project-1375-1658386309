from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bsb19147;PWD=M8Q6aCGQuLHwiHkU",'','')

@app.route('/')

def logreg():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('Login&Register', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    
    return render_template('Login&Register.html')

@app.route('/home',methods =['GET', 'POST'])

def home():
    return render_template('home.html')


@app.route('/donor',methods =['GET', 'POST'])

def donor():
    msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         
         phno= request.form['phno']
         addr = request.form['addr']
         bg = request.form['bg']
         sql = "SELECT * FROM users WHERE username =?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
            msg = ''
            return render_template('home.html', msg = msg)

         
         
         insert_sql = "INSERT INTO  PDA_DONOR VALUES (?, ?, ?, ?, ?)"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(prep_stmt, 1, username)
         ibm_db.bind_param(prep_stmt, 2, email)
         ibm_db.bind_param(prep_stmt, 3, phno)
         ibm_db.bind_param(prep_stmt, 4, addr)
         ibm_db.bind_param(prep_stmt, 5, bg)
         ibm_db.execute(prep_stmt)
         msg = 'You have successfully filled your details !'
         session['loggedin'] = True
         TEXT = "Hello sandeep,a new appliaction for job position" +jobs+"is requested"
         
         
    return render_template('donor.html')

@app.route('/success',methods =['GET', 'POST'])

def success():
    return render_template('success.html')

@app.route('/receiver',methods =['GET', 'POST'])

def receiver():
    if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         
         phno= request.form['phno']
         addr = request.form['addr']
         bg = request.form['bg']
         sql = "SELECT * FROM users WHERE username =?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
            msg = ''
            return render_template('home.html', msg = msg)
    return render_template('receiver.html')
#sendmail(TEXT,"alferedd34@gmail.com")
         sendgridmail("alferedd34@gmail.com",TEXT)

@app.route('/thirdparty',methods =['GET', 'POST'])

def thirdparty():
    return render_template('thirdparty.html')


if __name__ == '__main__':
   app.run(debug='True')
