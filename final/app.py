import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # getting the username
    username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = username2[0].get('username')

    # obtaining current prices for stocks
    stocks = db.execute("SELECT stock FROM portfolio WHERE user_id = ?", session["user_id"])
    number1 = db.execute("SELECT COUNT(*) FROM portfolio WHERE user_id = ?", session["user_id"])
    number = number1[0].get('COUNT(*)')

    # looping through the current prices, updating them for the user
    for i in range(0, number - 1, +1):
        # getting the stock
        stock = stocks[i].get('stock')

        # get the shares for that line
        rows2 = db.execute("SELECT MAX(transaction_id) FROM portfolio")
        rows = rows2[0].get('MAX(transaction_id)')  # number of rows

        # getting the number of shares
        sum_shares = db.execute(
            "SELECT SUM(shares) FROM portfolio WHERE stock = ? AND user_id = ?", stock, session["user_id"])
        sum_share = sum_shares[0].get('SUM(shares)')

        # getting the current price
        current = lookup(stock).get("price")

        # update the transaction table
        db.execute("UPDATE portfolio SET current = ? WHERE stock = ?", current, stock)

        # update total value
        for i in range(rows+1):
            shares = db.execute(
                "SELECT shares FROM portfolio WHERE stock = ? AND user_id = ? AND transaction_id = ?", stock, session["user_id"], i)
            if shares:
                share = shares[0].get('shares')
                curr_val = current * share  # this is grouped value
                db.execute("UPDATE portfolio SET curr_val = ? WHERE stock = ? AND user_id = ? AND transaction_id = ?",
                           curr_val, stock, session["user_id"], i)

    # group by stock for the user
    grouped = db.execute(
        "SELECT stock, current, SUM(shares) AS sum1, SUM(curr_val) AS sumcurr, price FROM portfolio WHERE user_id = ? GROUP BY stock HAVING SUM(shares) > 0", session["user_id"])

    total_cash2 = 0
    total_cash = 0
    total_balance = 0
    balance = 0

    # getting the total cash
    total_cash1 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total_cash2 = total_cash1[0].get('cash')
    if total_cash2:
        total_cash = usd(total_cash2)

    # getting the portfolio balance
    balance1 = db.execute(
        "SELECT SUM(curr_val) FROM portfolio WHERE user_id = ?", session["user_id"])
    balance2 = balance1[0].get("SUM(curr_val)")
    if balance2:
        balance = balance2
        total_balance = usd(balance)

    # getting total of everything
    total_cash_port = total_cash2 + balance
    total_cash_port = usd(total_cash_port)

    # returning back
    return render_template("index.html", usd=usd, grouped=grouped, username=username, total_cash=total_cash, total_balance=total_balance, total_cash_port=total_cash_port)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if POST
    if request.method == "POST":

        # gather symbol and shares data
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide an integer", 400)

        # if symbol is not input
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # if shares are not input
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # if shares are not positive integers
        if shares <= 0:
            return apology("must provide positive integer", 400)

        # if such symbol does not exist
        if lookup(symbol) == None:
            return apology("must provide an existing stock symbol", 400)

        # look up the symbol and stock price
        result = lookup(symbol).get("price")

        # determine the price of the purchase
        value = result * shares
        price = usd(value)

        # retrieve information about how much cash user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash1 = cash[0]
        cash2 = cash1.get('cash')
        cash2 = cash2 - value

        # if user does not have enough cash for the purchase
        if cash2 < 0:
            return apology("not enough funds", 403)

        remains = usd(cash2)

        # update the user table cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash2, session["user_id"])

        # creating the time of transaction
        time = db.execute("SELECT datetime('now')")
        time1 = time[0]
        time2 = time1.get("datetime('now')")

        # current price update, current value update
        current = result
        curr_val = value

        # type of the transaction
        transtype = 'Buy'

        # update SQL transaction table for user to store information
        db.execute("INSERT INTO portfolio (user_id, type, day, stock, price, current, shares, value, curr_val) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], transtype, time2, symbol, result, current, shares, value, curr_val)

        # updating the total
        total = db.execute("SELECT total FROM total WHERE user_id = ?", session["user_id"])
        total1 = total[0]
        new_total = total1.get('total')
        new_total = new_total + value
        db.execute("UPDATE total SET total = ? WHERE user_id = ?", new_total, session["user_id"])

        # redirect to completed
        return render_template('completed.html', symbol=symbol, shares=shares, price=price, remains=remains)

    # if GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])

    # implement usd

    return render_template("history.html", portfolio=portfolio, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # rendering stock's current price
    # entering the page
    if request.method == "GET":
        return render_template("quote.html")

    # gather data for the symbol via post
    if request.method == "POST":

        # gather data for the symbol
        symbol = request.form.get("symbol")

        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        if lookup(symbol) == None:
            return apology("must provide an existing stock symbol", 400)

        # look up the symbol and stock price
        result = lookup(symbol).get("price")

        price = usd(result)

        # redirect to Quoted
        return render_template("quoted.html", symbol=symbol, price=price)

    return apology("Something went wrong...", 403)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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
        ident = db.execute("SELECT id FROM users WHERE username = ?", username)
        ident2 = ident[0].get('id')
        db.execute("INSERT INTO total (user_id) VALUES(?)", ident2)

        # create new portfolio table for the user?

        # return to the login page
        return render_template("login.html")
    # else
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # if POST
    if request.method == "POST":

        # gather symbol and shares data
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide an integer", 403)

        # if symbol is not input
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)

        # if shares are not input
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        # if shares are not positive integers
        if shares <= 0:
            return apology("must provide positive integer", 403)

        # if such symbol does not exist
        if lookup(symbol) == None:
            return apology("must provide an existing stock symbol", 403)

        # look up the symbol and stock price
        result = lookup(symbol).get("price")

        # if the user does not have this stock
        stock = db.execute(
            "SELECT stock FROM portfolio WHERE type = 'Buy' AND user_id = ? AND stock = ?", session["user_id"], symbol)
        if not stock:
            return apology("user does not own this stock", 403)

        # if the user has fewer shares than requested
        # shares bought
        bshares = db.execute(
            "SELECT SUM(shares) FROM portfolio WHERE type = 'Buy' AND user_id = ? AND stock = ?", session["user_id"], symbol)
        if bshares:
            buyshares = bshares[0].get('SUM(shares)')
        else:
            buyshares = 0

        shares_owned = buyshares

        # shares sold
        sshares = db.execute(
            "SELECT SUM(shares) FROM portfolio WHERE type = 'Sell' AND user_id = ? AND stock = ?", session["user_id"], symbol)
        if sshares is not None:
            sellshares = sshares[0].get('SUM(shares)')
        else:
            sellshares = 0

        if sellshares is not None:
            shares_owned = shares_owned + sellshares

        # comparing the request to the existing shares
        if shares_owned < shares:
            return apology("not enough shares for this sale", 400)

        # determine the price of the sale
        value = result * shares
        price = usd(value)

        # retrieve information about how much cash user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash1 = cash[0].get('cash')

        # establishing remaining cash after the sale
        cash1 = cash1 + value  # returning cash to the user

        # update the user table cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash1, session["user_id"])

        remains = usd(cash1)

        # creating the time of transaction
        time = db.execute("SELECT datetime('now')")
        time2 = time[0].get("datetime('now')")

        # current price update, current value update
        current = result
        curr_val = value

        # type of the transaction
        transtype = 'Sell'

        # changing the sign for the sell shares to update in the table
        shares = -shares

        # update SQL transaction table for user to store information
        db.execute("INSERT INTO portfolio (user_id, type, day, stock, price, current, shares, value, curr_val) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], transtype, time2, symbol, result, current, shares, value, curr_val)

        # updating the total
        total = db.execute("SELECT total FROM total WHERE user_id = ?", session["user_id"])
        new_total = total[0].get('total')
        new_total = new_total - value
        db.execute("UPDATE total SET total = ? WHERE user_id = ?", new_total, session["user_id"])

        # redirect to Completed
        return render_template("completedsale.html", symbol=symbol, shares=shares, price=price, remains=remains)

    # if GET
    else:
        symbol = db.execute(
            "SELECT stock FROM portfolio WHERE type = 'Buy' AND user_id = ? GROUP BY stock HAVING SUM(shares) > 0", session["user_id"])

        return render_template("sell.html", symbol=symbol)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    # if POST
    if request.method == "POST":
        # request the amount from the user
        try:
            amount = int(request.form.get("cash"))
        # if not positive integer, decline
        except ValueError:
            return apology("must provide an integer", 403)

        # if more than 1,000,000,000, decline
        if amount > 1000000000:
            return apology("we don't support over a billion USD", 403)

        # retrieve current balance
        balance1 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        balance = balance1[0].get('cash')

        # inform the user about his new cash balance, add to the "users" table
        remains = balance + amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remains, session["user_id"])

        remains = usd(remains)
        amount = usd(amount)

        # finish with the template
        return render_template("cash_added.html", amount=amount, remains=remains)

    # if GET
    else:
        return render_template("cash.html")
