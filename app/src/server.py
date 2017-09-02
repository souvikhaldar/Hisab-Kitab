from src import app
from flask import jsonify, request
import requests
import json
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
#from flask_mysqldb import MySQL
#from data import Articles
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField
#from passlib.hash import sha256_crypt
from functools import wraps
global token
#check if logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, please log in','danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")


def user_info():
    url = 'http://auth.hasura/user/account/info'
    headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}
    d = requests.post(url, headers=headers)
    print(d)
    f=d.json()
    print(f)
    return f



class RegisterForm(Form):
	name=StringField('Name',[validators.Length(min=1,max=30)])
	username=StringField('Username',[validators.Length(min=1,max=100)])
	email=StringField('Email',[validators.Length(min=1,max=50)])
	password=PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm',message='Passwords do not match')
		])
	confirm=PasswordField('Confirm Password')

#article form
class ArticleForm(Form):
	expense=StringField('Expense',[validators.Length(min=1,max=300)])
	amount=IntegerField('Amount', [validators.NumberRange(min=0, max=10000000)])


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=form.password.data
        url = 'http://auth.c100.hasura.me/signup'
        data = {'username': username, 'password': password}
        headers = {'Content-Type' : 'application/json'}

        r = requests.post(url, data=json.dumps(data), headers=headers)
        a=r.json()
        #token=a['auth_token']

        #return json.dumps(r.json(), indent=4)
        #return r['auth_token']
        flash('You are now registered','success')
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

#login part
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username= request.form['username']
        password=request.form['password']
        #making request to login endpoint
        url = 'http://auth.hasura/login'
        data = {'username': username, 'password': password}
        headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}

        r = requests.post(url, data=json.dumps(data), headers=headers)
        a=r.json()
        try:
            message=a['message']
            print(message)
            error='Something is fishy! Try again.'
            flash(error,"warning")
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            token=a['auth_token']
            session['username']=username
            session['logged_in']=True
            flash("You are now logged in","success")
            print("the token is "+token)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


#register
@app.route('/dashboard',methods=['GET','POST'])
#@is_logged_in
def dashboard():
    url = 'http://data.hasura/v1/query'
    query = {
    "type": "select",
    "args": {
        "table": "expenditure",
        "columns": [
            "*"
        ]
    }
}
    headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}
    try:
        r = requests.post(url, data=json.dumps(query), headers=headers)
        print('The type is ',r)

        articles=r.json()
        return render_template('dashboard.html',articles=articles)

    except Exception as e:
        print(e)


#add article
@app.route('/add_expense',methods=['GET','POST'])
#@is_logged_in
def add_expense():
    form=ArticleForm(request.form)
    if request.method=='POST' and form.validate():
        expense=form.expense.data
        amount=form.amount.data

        url = 'http://data.hasura/v1/query'
        query = {  "type" : "insert",
         "args" : {
           "table"     : "expenditure",
           "objects"   : [
             {
               "expense"   : expense,
               "author":session['username'],
               "amount" : amount
             }
           ]
         }
      }
        headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}
        try:
            r = requests.post(url, data=json.dumps(query), headers=headers)
            print('The response is ',r)

            flash('expenditure listed','success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            print(e)


        '''
        #create cursor
        cur=mysql.connection.cursor()

        cur.execute("insert into articles(title,body,author) values(%s,%s,%s)",(expense,amount,session['username']))
        #commit
        mysql.connection.commit()
        #close connection
        cur.close()'''
    return render_template('add_article.html',form=form)



@app.route('/insights',methods=['POST','GET'])
def insights():
    url = 'http://data.hasura/v1/query'
    query = {
    "type": "select",
    "args": {
        "table": "insights",
        "columns": [
            "*"
        ]
    }
}
    headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}
    try:
        r = requests.post(url, data=json.dumps(query), headers=headers)
        print('The type is ',r)

        insights=r.json()
        print(insights)
        print(insights['maxi'])
        return render_template('insights.html',insights=insights)

    except Exception as e:
        print(e)

    '''
    #create cursor
    cur=mysql.connection.cursor()
    result=cur.execute("select sum(body) as sum from articles where author=%s",(session['username'],))
    insights=cur.fetchall()
    a=list(insights[0].values())
    result=cur.execute("select max(body) as maxi from articles where author=%s",(session['username'],))
    maxi=cur.fetchall()
    b=list(maxi[0].values())

    #identity=session['username']

    result=cur.execute("select min(body) as mini from articles where author=%s",(session['username'],))
    mini=cur.fetchall()
    c=list(mini[0].values())


    #if insights>0:
    return render_template('insights.html',insights=a[0],maxi=b[0],mini=c[0])
    #else:
     #   msg="No expense found"
      #  return render_template('insights.html',msg=msg)
    #close connection
    cur.close()
'''



#log out
@app.route('/logout')
#@is_logged_in
def logout():
    session.clear()
    url = 'http://auth.hasura/user/logout'
    headers = {'Content-Type' : 'application/json','X-Hasura-User-Id': '1','X-Hasura-Role': 'admin'}
    r = requests.post(url, headers=headers)
    a=r.json()
    print(a['message'])

    flash("You are now logged out",'success')
    return redirect(url_for('login'))
