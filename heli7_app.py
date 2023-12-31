import pymysql
from flask import Flask, render_template, request, redirect, url_for, session
import logging

# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired

app = Flask(__name__)


# Set the SECRET_KEY for your app


@app.route('/index', methods=['GET'])
def view_home():
    return render_template("index.html")


@app.route('/about_us', methods=['GET'])
def view_about():
    return render_template("about_us.html")


@app.route('/our_fleet', methods=['GET'])
def view_fleet():
    return render_template("our_fleet.html")


@app.route('/signup', methods=['GET'])
def view_sign():
    return render_template("signup.html")


@app.route('/login', methods=['GET'])
def view_login():
    return render_template("login.html")


@app.route('/contact_us', methods=['GET'])
def view_contact():
    return render_template("contact_us.html")


@app.route('/faq', methods=['GET'])
def view_faq():
    return render_template("faq.html")


@app.route('/gdpr', methods=['GET'])
def view_gdpr():
    return render_template("gdpr.html")


@app.route('/registration', methods=['GET'])
def view_registration():
    return render_template("registration.html")


@app.route('/reviews', methods=['GET'])
def make_review():
    return render_template("reviews.html")


@app.route('/our_fleet')
def our_fleet():
    return render_template('our_fleet.html')


@app.route('/thx_rev', methods=['GET'])
def thx_rev():
    return render_template("thx_rev.html")


@app.route('/privacy', methods=['GET'])
def view_privacy():
    return render_template("privacy.html")


app.config['SECRET_KEY'] = '0123456789'


def connection():
    server = 'localhost'
    # adrians database
    # db = 'heli7_project'
    db = 'Heli7'
    # pattricks database
    uid = 'sky'
    pwd = 'P@$$word'
    conn = pymysql.Connect(host=server, user=uid, password=pwd, database=db)
    conn.autocommit(True)
    return conn


@app.route('/registration', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        title = request.form["Title"]
        firstname = request.form["FirstName"]
        lastname = request.form["LastName"]
        doornumber = request.form["DoorNumber"]
        streetname = request.form["StreetName"]
        city = request.form["City"]
        postcode = request.form["PostCode"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        dob = request.form["DOB"]
        print(title, firstname, lastname, doornumber,
              streetname, city, postcode, email, phone, dob)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(
            "insert into customers(Title, FirstName, LastName, DoorNumber, StreetName, City, PostCode, email, phone, DOB) values ('" + title + "','" + firstname + "','" + lastname + "','" + doornumber + "','" + streetname + "','" + city + "','" + postcode + "','" + phone + "','" + email + "','" + dob + "')")
        return render_template('reg_confirm.html')
    return render_template("registration.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM login WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            login = cursor.fetchone()

        if login:
            session['username'] = username
            redirect(url_for('index'))
            return render_template("index.html", MSG="Welcome " + username)
        else:
            return render_template('Login.html', MSG="Logging Failed")
    return render_template('Login.html', MSG="")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    else:
        return redirect(url_for('index.html'))


@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        logging.info(f"Logged out: {username}")
        session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO login (username, email, password) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, email, password))
            conn.commit()  # Commit the transaction
            return redirect(url_for('success'))
        except Exception as e:
            conn.rollback()  # Roll back changes if an error occurs
            return render_template('signup.html', error=str(e))
        finally:
            conn.close()
            return render_template('signup_confirm.html', error=None)
    return render_template('signup.html', error=None)


@app.route('/book', methods=["GET", "POST"])
def book_trip():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        destination = request.form.get("destination")
        departure_date = request.form.get("departure_date")

        # To store in Database
        insert_query = """
            INSERT INTO bookings (name, email, destination, departure_date)
            VALUES (%s, %s, %s, %s)
        """
        data = (name, email, destination, departure_date)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, data)

        return render_template("payment.html")

    return render_template("book.html", MSG="Welcome")


@app.route('/payment', methods=["GET", "POST"])
def make_payment():
    if request.method == "POST":
        nameoncard = request.form.get("nameoncard")
        cardnumber = request.form.get("cardnumber")
        expmonth = request.form.get("expmonth")
        expyear = request.form.get("expyear")
        csv = request.form.get("csv")

        # To store in Database
        insert_query = """
            INSERT INTO cardpayment (nameoncard, cardnumber, expmonth, expyear, csv)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (nameoncard, cardnumber, expmonth, expyear, csv)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, data)

        return render_template("thank_you.html")
    return render_template("payment.html", MSG="Welcome")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    # Perform a search based on the 'query' parameter
    # You can use this query to search your database or perform any other search operation

    # For demonstration purposes, let's assume a simple list of results
    results = ['our_fleet.html']

    # Redirect to the desired HTML page if a result is found
    if results:
        # In this example, we'll redirect to 'our_fleet.html'
        return redirect(url_for('our_fleet'))

    # Handle the case when no results are found
    return render_template('no_results.html')


@app.route('/reviews', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        # Use parentheses, not square brackets
        review = request.form.get('review')
        # Use parentheses, not square brackets
        author = request.form.get('author')
        # Use parentheses, not square brackets
        date = request.form.get('date')
        # Use parentheses, not square brackets
        trip = request.form.get('trip')

        # Add code here to insert the review data into the MySQL database
        insert_query = "INSERT INTO reviews (review, author, date, trip) VALUES (%s, %s, %s, %s)"

        data = (review, author, date, trip)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, data)
        conn.commit()  # Commit the changes to the database
        cursor.close()
        conn.close()

    # Redirect to the home page or wherever you want
    return redirect(url_for('thx_rev'))


if __name__ == "__main__":
    app.run(port=5002)
