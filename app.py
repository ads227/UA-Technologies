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

@app.route('/post', methods = ['POST'])

def data():
    if request.method == 'POST':
        print('POST')
        form_data = request.form
        conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM event;")
        content = cur.fetchall()

        print(form_data["content"])
        return render_template('index.html', content = content)