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