from flask import Flask, render_template, request, redirect, session, url_for
from flask import current_app as app
import psycopg2
import requests
import msal
from flask_session import Session
from . import app_config
import json

# Load config file
app.config.from_object(app_config)

# Session to store auth token, maintain login
Session(app)

# Index
@app.route("/")
def hello():
  if not session.get("user"):
    return redirect(url_for("login"))
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("SELECT ytdearnings FROM department WHERE department='Athletics';")
  content = cur.fetchone()[0]
  return render_template('index.html', user=session["user"], profit=content)

# Loads if not logged in; provides login link for Microsoft account
@app.route("/login")
def login():
  session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
  return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

# Redirect after login, grab and cache oauth2 token
@app.route("/getAToken")
def authorized():
  cache = _load_cache()
  result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
    session.get("flow", {}), request.args)
  session["user"] = result.get("id_token_claims")
  _save_cache(cache)
  return redirect(url_for("hello"))

# Display all events
@app.route('/display', methods = ['GET'])
def data():
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("SELECT * FROM event;")
  contents = cur.fetchall()
  rows = len(contents)
  return render_template('display.html', content = contents, rows = rows)

# Render insert form
@app.route('/insert', methods = ['GET'])
def insert():
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("SELECT * FROM department WHERE department != 'Athletics';")
  contents = cur.fetchall()
  departments = len(contents)
  return render_template('insert.html', departments=contents, rows=departments)

# Perform event insert
@app.route('/append', methods = ['POST'])
def append():
  title = request.form['title']
  category = request.form['category']
  hours = request.form['hours']
  facility = request.form['facility']
  area = request.form['area']
  fee = request.form['fee']
  PFOC = request.form.get('PFOC', 0)
  athleticsMaintenance = request.form.get('AthleticsMaintenance', 0)
  athleticsCustodial = request.form.get('AthleticsCustodial', 0)
  ushers = request.form.get('Ushers', 0)
  trainers = request.form.get('Trainers', 0)
  parking = request.form.get('Parking', 0)
  police = request.form.get('Police', 0)
  sv = request.form.get('Sound/Video', 0)


  # Process date to expected format
  date = request.form['date']
  month, day, year = date.split("/")
  microsoftDateTime = year + "-" + month + "-" + day + "T12:00:00"

  # Get oauth2 token, ensure it is valid
  token = _get_token_from_cache(app_config.SCOPE)
  if not token:
    return redirect(url_for("login"))

  # Microsoft Graph API post request body for an Outlook Calendar Event
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

  # Convert request body to JSON
  body = json.dumps(content)

  # Make POST request
  graph_data = requests.post(
    app_config.ENDPOINT,
    body,
    headers={'Authorization': 'Bearer ' + token['access_token'], 'Content-Type': 'application/json'},
    ).json()

  # Insert event into database
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute('INSERT INTO event( title,category,hours,date,facilityName,facilityArea,rentalFee) VALUES(%s, %s, %s, %s, %s, %s, %s);', (title, category, hours, date, facility, area, fee))
  conn.commit()

  # Insert into eventstaffing intersection table
  # Get this eventid for foreign key
  cur.execute("SELECT eventid FROM event WHERE title='" + title +"' AND date='" + date + "';")
  eventid = int(cur.fetchone()[0])

  # Special case, Athletics always involved
  cur.execute("SELECT departmentid FROM department WHERE department='Athletics';")
  departmentid = str(cur.fetchone()[0])
  cur.execute("SELECT rentalFee FROM event WHERE title='" + title +"' AND date='" + date + "';")
  fee = cur.fetchone()[0]

  profit = fee - PFOC - float(athleticsMaintenance) - float(athleticsCustodial) - float(ushers) - float(trainers) - float(parking) - float(police) - float(sv)
  cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, profit))
  conn.commit()
  if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(profit) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()


  # Insert each valid department-event intersection. A 0 value indicates that department had no involvement/revenue.
  # Get departmentid, then use it to insert values to the intersection table. Also, add the department's earnings from
  # this event to their ytdearnings in the department table.
  if float(PFOC) > 0:
    print("PFOC: " + PFOC)
    cur.execute("SELECT departmentid FROM department WHERE department='PFOC';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, PFOC))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(PFOC) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(athleticsMaintenance) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='AthleticsMaintenance';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, athleticsMaintenance))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(athleticsMaintenance) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(athleticsCustodial) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='AthleticsCustodial';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, athleticsCustodial))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(athleticsCustodial) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(ushers) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='Ushers';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, ushers))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(ushers) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(trainers) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='Trainers';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, trainers))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(trainers) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(parking) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='Parking';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, parking))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(parking) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(police) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='Police';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, police))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(police) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  if float(sv) > 0:
    cur.execute("SELECT departmentid FROM department WHERE department='Sound/Video';")
    departmentid = str(cur.fetchone()[0])
    cur.execute('INSERT INTO eventstaffing(departmentid, eventid, earnings) VALUES(%s, %s, %s);', (departmentid, eventid, sv))
    conn.commit()
    if int(year) == 2022:
      cur.execute('UPDATE department SET ytdearnings = ytdearnings + ' + str(sv) + 'WHERE departmentid = ' + departmentid +';')
      conn.commit()
  return hello()

# Render update event page
@app.route('/update', methods = ['POST'])
def update():
  id = request.form.get('id')
  title = request.form.get('title')
  category = request.form.get('category')
  hours = request.form.get('hours')
  date = request.form.get('date')
  facility = request.form.get('facility')
  area = request.form.get('area')
  fee = request.form.get('fee')
  return render_template('update.html', title = title, category = category, hours = hours, date = date,
    facility = facility, area = area, fee = fee, id=id)

# Perform event update
@app.route('/updateSubmit', methods = ['POST'])
def updateSubmit():
  id = request.form.get('id')
  title = request.form.get('title')
  category = request.form.get('category')
  hours = request.form.get('hours')
  date = request.form.get('date')
  facility = request.form.get('facility')
  area = request.form.get('area')
  fee = request.form.get('fee')

  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("UPDATE event SET title = %s, category = %s, hours = %s, date = %s, facilityname = %s, facilityarea = %s, rentalfee = %s where eventid = %s;",
   (title, category, hours, date, facility, area, fee, id))
  conn.commit()
  cur.execute("SELECT * FROM event;")
  contents = cur.fetchall()
  rows = len(contents)

  return render_template('display.html', content = contents, rows = rows)

# Delete event
@app.route('/delete', methods = ['POST'])
def delete():
  id = str(request.form.get('id'))
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()

  # Remove proceeds from this event from department's ytdearnings
  cur.execute("SELECT date FROM event where eventid='" + id +"';")
  date = str(cur.fetchone()[0])
  year, month, day = date.split("-")

  if year == "2022":
    cur.execute("SELECT * FROM eventstaffing where eventid='" + id +"';")
    for element in cur.fetchall():
      departmentid = str(element[0])
      earnings = str(element[3])
      cur.execute('UPDATE department SET ytdearnings = ytdearnings - ' + earnings + 'WHERE departmentid = ' + departmentid +';')

  # Delete event, cascades to eventstaffing
  cur.execute("DELETE FROM event where eventid = %s;", (str(id),))
  conn.commit()
  cur.execute("SELECT * FROM event;")
  contents = cur.fetchall()
  rows = len(contents)

  return render_template('display.html', content = contents, rows = rows)

# Render search page
@app.route('/search', methods = ['POST'])
def search():
  return render_template('search.html')

# Search events by title
@app.route('/searchresult', methods = ['POST'])
def result():
  title = request.form.get('title')
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("SELECT * FROM event WHERE title = %s;", (title,))
  contents = cur.fetchall()
  rows = len(contents)
  return render_template('display.html', content = contents, rows = rows)

# Log out of Microsoft account
@app.route("/logout")
def logout():
  session.clear()  # Wipe out user and its token cache from session
  return redirect(  # Also logout from the tenant's web session
    app_config.AUTHORITY + "/oauth2/v2.0/logout" +
    "?post_logout_redirect_uri=" + url_for("hello", _external=True))

@app.route('/department', methods = ['GET'])
def departmentDisplay():
  conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
  cur = conn.cursor()
  cur.execute("SELECT * FROM department;")
  content = cur.fetchall()
  rows = len(content)
  return render_template('departments.html', content=content, rows=rows)

# Load cache to access token
def _load_cache():
  cache = msal.SerializableTokenCache()
  if session.get("token_cache"):
    cache.deserialize(session["token_cache"])
  return cache

# Save token to cache
def _save_cache(cache):
  if cache.has_state_changed:
    session["token_cache"] = cache.serialize()

# Allows validate via Azure Active Directory
def _build_msal_app(cache=None, authority=None):
  return msal.ConfidentialClientApplication(
    app_config.CLIENT_ID, authority=app_config.AUTHORITY,
    client_credential=app_config.CLIENT_SECRET, token_cache=cache)

# Azure Active Directory helper, allows "flow" paradigm for authentication
def _build_auth_code_flow(authority=None, scopes=None):
  return _build_msal_app(authority=authority).initiate_auth_code_flow(
    scopes,
    redirect_uri=url_for("authorized", _external=True))

# Load and return token in 1 function call, allows authentication without forcing another login
def _get_token_from_cache(scope=None):
  cache = _load_cache()  # This web app maintains one cache per session
  cca = _build_msal_app(cache)
  accounts = cca.get_accounts()
  if accounts:  # So all account(s) belong to the current signed-in user
    result = cca.acquire_token_silent(scope, account=accounts[0])
    _save_cache(cache)
    return result
