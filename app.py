from flask import Flask,render_template, request,redirect,url_for
import mysql.connector
import datetime

app = Flask(__name__)
conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='dragon',
        database='anime_database'
    )



#Displays the home page of the website
@app.route('/')
def home():
    return render_template('home.html')

#iF the user clicks on "Add Anime" It will display the add_anime page
@app.route('/add', methods=['GET','POST'])
def add_anime():
#Pulls the anime names from the cruncyroll database and displays the anime name in a drop down for the user to select
    cursor = conn.cursor()
    cursor.execute("SELECT anime FROM crunchyroll")
    anime_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
#pulls all values inputed by the user
    if request.method == 'POST':
        anime=request.form['anime']
        rating=request.form['rating']
        complete=request.form['completed']
        comment=request.form['comment']
        time=datetime.datetime.now()
        formatted_datetime = time.strftime("%Y-%m-%d %I:%M:%S %p")
        last_update = formatted_datetime
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user (anime,rating,completed,comment,last_updated) values(%s,%s,%s,%s,%s)',(anime,rating,complete,comment,last_update))
        conn.commit()
        return redirect(url_for('home',message='Anime Added Successfully!'))
    return render_template('add_anime.html', anime_names=anime_names)

#Displays the view_list page if the user wants to see their list
@app.route('/view')
def view_anime():
    cursor=conn.cursor()
    cursor.execute("select * from user")
    user=cursor.fetchall()

    
    return render_template('view_your_list.html',user=user)
    
    

#Deleted the anime entry
@app.route('/delete/<int:id>',methods=['GET'])
def delete_anime(id):
    cursor=conn.cursor()
    cursor.execute('DELETE from user where id=%s',(id,))
    conn.commit()
    return redirect(url_for('view_anime'))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update_anime(id):
    cursor= conn.cursor()
    if request.method == 'POST':
        rating=request.form['rating']
        complete=request.form['completed']
        comment=request.form['comment']
        time=datetime.datetime.now()
        formatted_datetime = time.strftime("%Y-%m-%d %I:%M:%S %p")
        last_update = formatted_datetime
        cursor = conn.cursor()
        cursor.execute('UPDATE user set rating=%s, completed=%s, comment=%s, last_updated=%s where id=%s',(rating,complete,comment,last_update,id))
        conn.commit()
        return redirect(url_for('view_anime'))
    cursor.execute('select * from user where id=%s',(id,))
    user=cursor.fetchone()
    return render_template('update_anime.html',user=user)


#Displays the the anime available on cruncyroll
@app.route('/viewcruncyroll')
def view_cruncyroll():
    cursor=conn.cursor()
    cursor.execute("select * from crunchyroll")
    user=cursor.fetchall()
    return render_template('view_crunchyroll.html',user=user)

if __name__=='__main__':
    app.run(debug=True)