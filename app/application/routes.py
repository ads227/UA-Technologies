from flask import Flask, render_template, request, redirect, session, url_for
from flask import current_app as app
from sqlite3 import Binary
import psycopg2
import uuid
import requests
import msal
from flask_session import Session
from . import app_config
import json

app.config.from_object(app_config)
Session(app)

@app.route("/")
def hello():
  print("hello")
  if not session.get("user"):
        return redirect(url_for("login"))
  return render_template('index.html', user=session["user"])

@app.route("/login")
def login():
  session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
  return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route("/getAToken")  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
  cache = _load_cache()
  result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
      session.get("flow", {}), request.args)
  print(result)
  session["user"] = result.get("id_token_claims")
  _save_cache(cache)
  return redirect(url_for("hello"))

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
    title = request.form['title']
    category = request.form['category']
    hours = request.form['hours']
    date = request.form['date']
    month, day, year = date.split("/")
    microsoftDateTime = year + "-" + month + "-" + day + "T12:00:00"
    facility = request.form['facility']
    area = request.form['area']
    overhead = request.form['overhead']
    fee = request.form['fee']
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    content = {
    "subject": title,
    "body": {
        "contentType": "HTML",
        "content": ""
    },
    "start": {
        "dateTime": microsoftDateTime,
        "timeZone": "Eastern Standard Time"
    },
    "end": {
        "dateTime": microsoftDateTime,
        "timeZone": "Eastern Standard Time"
    },
    "location": {
        "displayName": facility + " - " + area
    },
    }
    body = json.dumps(content)
    graph_data = requests.post(  # Use token to call downstream service
        app_config.ENDPOINT,
        body,
        headers={'Authorization': 'Bearer ' + token['access_token'], 'Content-Type': 'application/json'},
        ).json()
    print(graph_data)
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

@app.route("/logout")
def logout():
  session.clear()  # Wipe out user and its token cache from session
  return redirect(  # Also logout from your tenant's web session
    app_config.AUTHORITY + "/oauth2/v2.0/logout" +
    "?post_logout_redirect_uri=" + url_for("hello", _external=True))

def _load_cache():
  cache = msal.SerializableTokenCache()
  if session.get("token_cache"):
    cache.deserialize(session["token_cache"])
  return cache

def _save_cache(cache):
  if cache.has_state_changed:
    session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
  return msal.ConfidentialClientApplication(
    app_config.CLIENT_ID, authority=app_config.AUTHORITY,
    client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
  return _build_msal_app(authority=authority).initiate_auth_code_flow(
    scopes,
    redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
  cache = _load_cache()  # This web app maintains one cache per session
  cca = _build_msal_app(cache)
  accounts = cca.get_accounts()
  if accounts:  # So all account(s) belong to the current signed-in user
    result = cca.acquire_token_silent(scope, account=accounts[0])
    _save_cache(cache)
    return result


app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template