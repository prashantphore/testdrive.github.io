from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_mail import Mail
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'firstwebsite'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', params=params)

@app.route('/index')
def home():
    return render_template('index.html', params=params)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/services')
def services():
    return render_template('services.html', params=params)


@app.route('/sedan')
def sedan():
    return render_template('sedan.html', params=params)

@app.route('/x_series')
def x_series():
    return render_template('x_series.html', params=params)

@app.route('/m_series')
def m_series():
    return render_template('m_series.html', params=params)

@app.route('/404')
def error():
    return render_template('404.html', params=params)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', params=params)

@app.route('/login')
def login():
    return render_template('login.html', params=params)

@app.route('/option',methods=['GET','POST'])
def option():
        return render_template('option.html',params=params)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.method=="POST":
        cur = mysql.connection.cursor()
        cur.execute("select * from contact")
        r=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('dashboard.html', params=params,contact=r)
    else:
        cur = mysql.connection.cursor()
        cur.execute("select * from booking")
        r = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('dashboard.html', params=params,booking=r)


@app.route('/dashboard2', methods=['GET', 'POST'])
def dashboard2():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("select * from booking")
        a = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('dashboard2.html', params=params, booking=a)
    else:
        cur = mysql.connection.cursor()
        cur.execute("select * from contact")
        a = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('dashboard2.html', params=params,contact=a)


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        details = request.form
        name = details['name']
        phone = details['phone']
        email = details['email']
        message = details['msg']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact(name, phone, email) VALUES (%s, %s, %s, %s)", (name, phone ,email,message))
        mysql.connection.commit()
        mail.send_message('new message from ' + name,
                          sender= email,
                          recipients= [params['gmail-user']],
                          body= phone)
        cur.close()
    return render_template('contact.html', params=params)


@app.route('/requestdrive', methods=['GET','POST'])
def requestdrive():
    if request.method == "POST":
        details = request.form.get
        first_name = details('fname')
        last_name = details('lname')
        email = details('email')
        phone = details('phone')
        model = details('model')
        city = details('city')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO booking(fname,lname, email,phone, model,city) "
                    "VALUES (%s, %s, %s, %s , %s, %s)", [first_name, last_name, email, phone, model, city])
        mysql.connection.commit()
        mail.send_message('new message from '+first_name + ' '+ last_name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body='Model: '+ model + "\n"+ 'City: ' + city + "\n"+'Contact number: ' + phone)
        cur.close()
    return render_template('requestdrive.html', params=params)



if __name__ == '__main__':
    app.run(debug=True)