import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, bbl_heroku
import googlemaps
from geocoding import geocode, reverse_geocode
from site_info import zimas_info, zola_info

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///map.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# showing options for user
@app.route("/")
@login_required
def index():

    # getting the username
    username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = username2[0].get('username')

    # getting the project name and project_id
    status = "Active"
    grouped = db.execute("SELECT title, project_id FROM projects WHERE user_id = ? AND status = ?", session["user_id"], status)

    # returning back
    return render_template("userhome.html", username=username, grouped=grouped)

# showing the list of projects for user and greeting the user
@app.route("/list")
@login_required
def list():

    # getting the username
    username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = username2[0].get('username')

    # desired status
    status = "Active"

    # getting the project name
    grouped = db.execute("SELECT title, project_id, address, date_changed, authority, latitude, longitude FROM projects WHERE user_id = ? AND status = ?", session["user_id"], status)

    # returning back
    return render_template("list.html", username=username, grouped=grouped)

# bring to the website's home page
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

# showing the account information for user
@app.route("/account")
@login_required
def account():

    # getting the username
    username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = username2[0].get('username')

    # desired status
    status = "Active"
    status2 = "Deleted"

    # count of active projects
    count2 = db.execute("SELECT COUNT(*) FROM projects WHERE user_id = ? AND status = ?", session["user_id"], status)
    count = count2[0].get('COUNT(*)')

    # count of deleted projects
    deleted2 = db.execute("SELECT COUNT(*) FROM projects WHERE user_id = ? AND status = ?", session["user_id"], status2)
    deleted = deleted2[0].get('COUNT(*)')

    # returning back
    return render_template("account.html", username=username, count=count, deleted=deleted)


# redirect to the new project page, also add new project to portfolio
@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        # getting the username
        username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username2[0].get('username')

        # returning back
        return render_template("new.html", username=username)

    # if POST
    else:

        # gather name of project and title
        name = request.form.get("name")
        address = request.form.get("address")

        # if name is not input
        if not request.form.get("name"):
            return apology("must provide name of the project", 400)

        # if address is not input
        if not request.form.get("address"):
            return apology("must provide address of the project", 400)

        # creating the time of project creation
        time = db.execute("SELECT datetime('now')")
        time1 = time[0]
        time = time1.get("datetime('now')")

        # adding status to the new project
        status = "Active"

        # obtaining latitude longitude / verifying the validity
        gmaps = googlemaps.Client(key='AIzaSyCVaQ94dl2C-c2z83rAKSmmEfU5Mg4e1p8')
        geocode_result = gmaps.geocode(address)

        # if address is invalid, return an error
        if not geocode_result:
            return apology("provide a valid address")

        # obtaining coordinates from the geocode function
        geo = geocode_result[0]
        geo1 = geo.get('geometry')
        geo2 = geo1.get('location')
        lat = geo2.get('lat')
        lng = geo2.get('lng')

        # look up the address and decide which jurisdiction it is
        authority = lookup(address).get("authority")

        # update the projects table tying project to user
        db.execute("INSERT INTO projects (user_id, title, address, date_created, date_changed, authority, status, latitude, longitude) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name, address, time, time, authority, status, lat, lng)

        # retrieve project_id
        project_id2 = db.execute("SELECT project_id FROM projects WHERE user_id = ? AND title = ? AND date_created = ?", session["user_id"], name, time)
        project_id = project_id2[0].get('project_id')

        # if Zimas, then include sitespecs, if not, then include None in the table
        # each project should be in both tables
        if authority == "The City of Los Angeles":
            sitespecs = zimas_info(address)
        elif authority == "New York City":
            sitespecs = zola_info(address)
        else:
            sitespecs = {
                'Area':'NA',
                'Parcel':'NA',
                'Zoning':'NA',
                'Year':'NA',
                'Width':'NA',
                'Depth':'NA',
                'Address':address
            }

        # incorporating new site specs into the second table
        db.execute("INSERT INTO projectinfo (project_id, address, area, parcel, zoning, year, width, depth) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", project_id, sitespecs['Address'],
                   sitespecs['Area'], sitespecs['Parcel'], sitespecs['Zoning'], sitespecs['Year'], sitespecs['Width'], sitespecs['Depth'])

        # getting the username
        username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username2[0].get('username')

        # getting the project name
        grouped = db.execute("SELECT title FROM projects WHERE user_id = ?", session["user_id"])

        # redirect back to user home
        return render_template('userhome.html', username=username, grouped=grouped)


# GET is for looking at the project page, POST is for changing the project
@app.route("/project/<int:project_id>", methods=["GET", "POST"])
@login_required
def project(project_id):
    # if POST
    if request.method == "POST":
        # gather notes
        notes = request.form.get("notes")

        # gather name and address to change
        name = request.form.get("name")
        address = request.form.get("address")

        # creating the time of changing the project
        time = db.execute("SELECT datetime('now')")
        time1 = time[0]
        time = time1.get("datetime('now')")

        # update values in the table
        db.execute("UPDATE projects SET title = ?, date_changed = ?, notes = ? WHERE project_id = ?", name, time, notes, project_id)

        # getting the username
        username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username2[0].get('username')

        # getting the project name
        grouped = db.execute("SELECT title FROM projects WHERE user_id = ?", session["user_id"])

        print(f"Address: {address}")

        if address is None:
            # redirect back to user home
            return redirect(url_for('project', project_id=project_id, username=username, grouped=grouped))


        # if the user changed the address
        if address:
            print("Address is not none or empty")
            gmaps = googlemaps.Client(key='AIzaSyCVaQ94dl2C-c2z83rAKSmmEfU5Mg4e1p8')
            geocode_result = gmaps.geocode(address)

            # if address is invalid, return an error
            if not geocode_result:
                return apology("provide a valid address")

            # obtaining coordinates from the geocode function
            geo = geocode_result[0]
            geo1 = geo.get('geometry')
            geo2 = geo1.get('location')
            lat = geo2.get('lat')
            lng = geo2.get('lng')

             # look up the address and decide which jurisdiction it is
            authority = lookup(address).get("authority")

            # if Zimas or Zola, then include sitespecs, if not, then include None in the table
            if authority == "The City of Los Angeles":
                sitespecs = zimas_info(address)
            elif authority == "New York City":
                sitespecs = zola_info(address)
            else:
                sitespecs = {
                    'Area':'NA',
                    'Parcel':'NA',
                    'Zoning':'NA',
                    'Year':'NA',
                    'Width':'NA',
                    'Depth':'NA',
                    'Address':address
                }

            # update the projects table tying project to user
            db.execute("UPDATE projects SET address = ?, authority = ?, latitude = ?, longitude = ? WHERE project_id = ?", address, authority, lat, lng, project_id)

            # update projectinfo table if address had changed
            db.execute("UPDATE projectinfo SET address = ?, area = ?, parcel = ?, zoning = ?, year = ?, width = ?, depth = ? WHERE project_id = ?", sitespecs['Address'],
                   sitespecs['Area'], sitespecs['Parcel'], sitespecs['Zoning'], sitespecs['Year'], sitespecs['Width'], sitespecs['Depth'], project_id)

            # getting the site specs
            projectinfo = db.execute("SELECT * FROM projectinfo WHERE project_id = ?", project_id)

            # getting the notes
            notes = db.execute("SELECT notes FROM projects WHERE project_id = ?", project_id)

            # redirect back to user home
            return redirect(url_for('project', project_id=project_id, username=username, grouped=grouped, projectinfo=projectinfo, notes=notes))

    else:
        # getting the name of the project
        project = db.execute("SELECT title FROM projects WHERE project_id = ?", project_id)
        title = project[0].get('title')

        username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username2[0].get('username')

        lat2 = db.execute("SELECT latitude FROM projects WHERE project_id = ?", project_id)
        lat = lat2[0].get('latitude')

        lng2 = db.execute("SELECT longitude FROM projects WHERE project_id = ?", project_id)
        lng = lng2[0].get('longitude')

        address1 = db.execute("SELECT address FROM projects WHERE project_id = ?", project_id)
        address = address1[0].get('address')

        authority2 = db.execute("SELECT authority FROM projects WHERE project_id = ?", project_id)
        authority = authority2[0].get('authority')

        # getting the site specs
        projectinfo = db.execute("SELECT * FROM projectinfo WHERE project_id = ?", project_id)

        # getting the notes
        notes = db.execute("SELECT notes FROM projects WHERE project_id = ?", project_id)

        # returning back
        return render_template("project.html", authority=authority, project_id=project_id, address=address, project=project, title=title, username=username, lat=lat, lng=lng, projectinfo=projectinfo, notes=notes)

    return redirect(url_for('project', project_id=project_id, username=username, grouped=grouped))

# deleting the project (changing the status to "deleted")
@app.route("/delete/<int:project_id>")
@login_required
def delete(project_id):

    status = "Deleted"

    # update status in the table
    db.execute("UPDATE projects SET status = ? WHERE project_id = ?", status, project_id)

    title1 = db.execute("SELECT title FROM projects WHERE project_id = ?", project_id)
    title = title1[0].get('title')

    return render_template("delete.html", title=title)

# inquiring about a new site
@app.route("/inquiry", methods=["GET", "POST"])
@login_required
def inquiry():
    # this is an inquiry into a site
    if request.method == "POST":
        # gather address of the project
        address = request.form.get("address")

         # obtaining latitude longitude / verifying the validity
        gmaps = googlemaps.Client(key='AIzaSyCVaQ94dl2C-c2z83rAKSmmEfU5Mg4e1p8')
        geocode_result = gmaps.geocode(address)

        # if address is invalid, return an error
        if not geocode_result:
            return apology("provide a valid address")

        # obtaining coordinates from the geocode function
        geo = geocode_result[0]
        geo1 = geo.get('geometry')
        geo2 = geo1.get('location')
        lat = geo2.get('lat')
        lng = geo2.get('lng')

        # render the template
        return render_template("inquiry.html", lat=lat, lng=lng, address=address)

    # if GET
    else:
        # returning back
        return render_template("inquiry.html")


# logging in
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# logging out
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# registering
@app.route("/register", methods=["GET", "POST"])
def register():

    # if method post (user wants to register)
    if request.method == "POST":

        # collect information via form
        username = request.form.get("username")
        password = request.form.get("password")
        repeat_password = request.form.get("confirmation")

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # if passwords do not match
        elif not password == repeat_password:
            return apology("passwords must match", 400)

        # checking for existing usernames
        usernames1 = db.execute("SELECT username FROM users")
        if usernames1 is not None:
            rows1 = db.execute("SELECT COUNT(*) FROM users")
            rows = rows1[0].get('COUNT(*)')
            for i in range(0, rows, +1):
                usernames = usernames1[i].get('username')
                if username == usernames:
                    return apology("username already exists", 400)

        # insert user into the SQL database
        pwhash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pwhash)

        # log user in
        return redirect("/")
    # else
    else:
        return render_template("register.html")


