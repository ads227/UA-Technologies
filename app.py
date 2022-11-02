# DBM Term Project
# UA-Technologies
# Andrew Santa and Danielle Harris

from sqlite3 import Binary
from flask import Flask
from flask import render_template
from flask import request
import csv
import psycopg2

app = Flask(__name__)

@app.route('/')

def hello(name = None):
    return render_template('index.html', name = name)

@app.route('/display', methods = ['GET'])

def data():
    if request.method == 'GET':
        conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM event;")
        contents = cur.fetchall()
        rows = len(contents)
        return render_template('display.html', content = contents, rows = rows)

@app.route('/insert', methods = ['GET'])

def insert():
    return render_template('insert.html')

@app.route('/append', methods = ['POST'])

def append():
    print(request.form["title"])
    title = request.form['title']
    category = request.form['category']
    hours = request.form['hours']
    date = request.form['date']
    facility = request.form['facility']
    area = request.form['area']
    overhead = request.form['overhead']
    fee = request.form['fee']

    conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
    cur = conn.cursor()
    cur.execute('INSERT INTO event( title,category,hours,date,facilityName,facilityArea,overhead,rentalFee) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);', (title, category, hours, date, facility, area, overhead, fee))
    conn.commit()
    return render_template('index.html', success=True)

@app.route('/update', methods = ['POST'])

def update():
    id = request.form.get('id')
    title = request.form.get('title')
    category = request.form.get('category')
    hours = request.form.get('hours')
    date = request.form.get('date')
    facility = request.form.get('facility')
    area = request.form.get('area')
    overhead = request.form.get('overhead')
    fee = request.form.get('fee')
    return render_template('update.html', title = title, category = category, hours = hours, date = date, facility = facility, area = area, overhead = overhead, fee = fee, id=id)

@app.route('/updateSubmit', methods = ['POST'])

def updateSubmit():
    id = request.form.get('id')
    title = request.form.get('title')
    category = request.form.get('category')
    hours = request.form.get('hours')
    date = request.form.get('date')
    facility = request.form.get('facility')
    area = request.form.get('area')
    overhead = request.form.get('overhead')
    fee = request.form.get('fee')
    conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
    cur = conn.cursor()
    cur.execute("UPDATE event SET title = %s, category = %s, hours = %s, date = %s, facilityname = %s, facilityarea = %s, overhead = %s, rentalfee = %s where eventid = %s;", (title, category, hours, date, facility, area, overhead, fee, id))
    conn.commit()
    cur.execute("SELECT * FROM event;")
    contents = cur.fetchall()
    rows = len(contents)
    return render_template('display.html', content = contents, rows = rows)

@app.route('/delete', methods = ['POST'])

def delete():
    id = request.form.get('id')
    print(id)
    conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
    cur = conn.cursor()
    cur.execute("DELETE FROM event where eventid = %s;", (str(id),))
    conn.commit()
    cur.execute("SELECT * FROM event;")
    contents = cur.fetchall()
    rows = len(contents)
    return render_template('display.html', content = contents, rows = rows)

@app.route('/search', methods = ['POST'])

def search():
    return render_template('search.html')

@app.route('/searchresult', methods = ['POST'])

def result():
    title = request.form.get('title')
    print(title)
    conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
    cur = conn.cursor()
    cur.execute("SELECT * FROM event WHERE title = %s;", (title,))
    contents = cur.fetchall()
    rows = len(contents)
    return render_template('display.html', content = contents, rows = rows)