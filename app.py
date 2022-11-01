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
    return render_template('hello.html', name = name)

@app.route('/display', methods = ['POST'])

def data():
    if request.method == 'POST':
        conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM event;")
        contents = cur.fetchall()
        rows = len(contents)
        return render_template('display.html', content = contents, rows = rows)