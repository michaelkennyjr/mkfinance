import os
import psycopg2
from tempfile import mkdtemp
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application and auto-reload templates
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Don't cache responses
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem instead of signed cookies
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
# Have to figure out how to use Heroku to get correct URL
# Should I wait until I'm actually querying to do this, so I can close it too?
DATABASE_URL = os.environ["DATABASE_URL"]
conn = psycopg2.connect(DATABASE_URL, sslmode="require")

# Open a cursor to perform database operations
# Should I wait until I'm actually querying to do this, so I can close it too?
cur = conn.cursor()

@app.route("/")
def index():
    return render_template("form.html")
    
@app.route("/listcateg")
def listcateg():
    # Get ID of category type from name
    # I could do a separate query, but unless I plan on adding more it's not worth it
    ctinput = request.form.get("type")
    ctlist = {'Income': 0, 'Expense': 1, 'Transfer': 2}
    cattypeid = ctlist[ctinput]
    
    # Get list of categories of this type
    categories = []
    cur.execute("SELECT name FROM transactions WHERE type = %i;", cattypeid)
    for row in cur:
        categories.append(row[0])
        
    # Return list of categories as HTML piece
    return render_template("categories.html", categories=categories)
