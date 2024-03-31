from flask import Flask,render_template, request,redirect,url_for
import mysql.connector

app = Flask(__name__)

conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='dragon',
        database='anime_database'
    )
conn_user_database=mysql.connector.connect(
        host='localhost',
        user='root',
        password='dragon',
        database='user'   
)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/add', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        name=request.form['name']
        rating=request.form['rating']
        complete=request.form['complete']
        comment=request.form['comment']
        cursor = conn_user_database.cursor()
        cursor.execute('INSERT INTO users (name,rating,complete,comment) values(%s,%s,%s,%s)',(name,rating,complete,comment))
        conn_user_database.commit()
        return redirect(url_for('home',message='Student Added Successfully!'))
    return render_template('add_anime.html')