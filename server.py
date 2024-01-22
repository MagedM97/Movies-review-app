from flask import Flask, render_template, url_for, request, redirect, flash, session
import math
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# User class for handling user authentication
class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def find_by_email_and_password(email, password):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and check_password_hash(user_data[3], password):
            return User(user_data[0], user_data[1], user_data[2])
        else:
            return None

# Function to get suggestions from a file
def get_suggestions():
    suggestions = open("./static/data/suggestions.txt")
    content = suggestions.read()
    suggestions.close()
    all_suggestions = content.split("\n") 
    all_suggestions.pop()
    return all_suggestions

# Function to append a suggestion to the file
def append_suggestion(suggestion):
    suggestions = open("./static/data/suggestions.txt","a")
    suggestions.write(suggestion+"\n")
    suggestions.close()

app = Flask(__name__)




app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'movies'  

app.config['SECRET_KEY'] = 'your-secret-key'  

mysql = MySQL(app)


# Route for the home page
@app.route("/")
def index():
    cur = mysql.connection.cursor()

    # Getting query params
    category = request.args.get('type')  
    date = request.args.get('latest')  
    year = request.args.get("year")  
    name = request.args.get("movie-name")  
    page = request.args.get('page',1 ,type=int)
    per_page = 8
    start = (page - 1)*per_page
    end = start + per_page

    # Retrieving movies according to query params
    if category:
        # Retrieve movies based on the specified category
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE categories.name = %s GROUP BY movies.id", (category,))
        movies = cur.fetchall()
    elif date:
        # Retrieve movies based on the latest release date
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.release_date >= '2023-01-01'  GROUP BY movies.id")
        movies = cur.fetchall()
    elif year and name:
        # Retrieve movies based on the specified year and movie name
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE YEAR(movies.release_date) = %s AND movies.name LIKE %s  GROUP BY movies.id",(year,'%' + name +'%'))
        movies = cur.fetchall()
    elif name:
        # Retrieve movies based on the specified movie name
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.name LIKE %s  GROUP BY movies.id",('%' + name +'%',))
        movies = cur.fetchall()
    elif year:
        # Retrieve movies based on the specified year
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE  YEAR(movies.release_date) = %s GROUP BY movies.id",(year,))
        movies = cur.fetchall()
    else:
        # Retrieve all movies
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id GROUP BY movies.id")
        movies = cur.fetchall()

    # Retrieve all categories
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.close()
    total_pages = math.ceil((len(movies) / per_page))
    movies_on_page = movies[start:end]
    # Add active class to the navigation based on the query parameters
    if category:
        return render_template("index.html", movies=movies, categories=categories, active='category', type=category)
    elif date:
        return render_template("index.html", movies=movies, categories=categories, active='latest')
    else:
        return render_template("index.html", movies=movies_on_page, categories=categories, active='home',total_pages=total_pages,page=page)


# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Call the static method to find the user by email and password
        user = User.find_by_email_and_password(email, password)

        if user:
            # Set session variables for logged-in user
            session['logged_in'] = True
            session['username'] = user.username
            session['id'] = user.id

            return redirect(url_for("index"))
        else:
            flash('Username or Password Incorrect', "message")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            if not username or not password or not email:
                flash("Please fill in all the fields", "message")
                return redirect(url_for("register"))

            cur = mysql.connection.cursor()

            # Check if the email already exists in the database
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user:
                flash("Email already exists. Please use a different email.", "message")
                return redirect(url_for("register"))

            # Execute query to insert user into the database
            password_hash = generate_password_hash(password)
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password_hash, email))
            mysql.connection.commit()

            
            cur.close()

            flash("Successful Registration", "message")
            return redirect(url_for("login"))

        except:
            flash("An error occurred. Please try again.", "message")
            return redirect(url_for("register"))

    return render_template("register.html")

# Route for the logout page
@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# Route for the watch-list page
@app.route('/watch-list')
def watch_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    return render_template("watch-list.html", categories=categories, active='watch-list')

# Route for adding rate
@app.route('/rate',methods=["GET","POST"])
def rate():
    movie_id = request.form["movieId"]
    rate = request.form["rate"]
    if request.method == "POST":
        try:
            # Check if user has entered a rating for the selected movie before 
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM ratings WHERE movie_id = %s AND user_id = %s", (movie_id, session["id"]))
            old = cur.fetchone()
            if old:
               flash("Your Already added you rate For this Movie", "message")
               return redirect(request.referrer) 
             # Add user's rating  
            cur.execute("INSERT INTO ratings (movie_id, user_id, rating) VALUES (%s, %s, %s)", (movie_id, session["id"], rate))
            mysql.connection.commit()
            cur.close()
            flash("Your Rate added successfully", "message")
            return redirect(request.referrer)
        except:
            flash("Something went wrong, Try again", "message")
            return redirect(request.referrer)


# Route for adding review        
@app.route('/review',methods=["GET","POST"])
def review():
    movie_id = request.form["movieId"]
    review = request.form["review"]
    if request.method == "POST":
        try:
            cur = mysql.connection.cursor()
            
            # Check if user has entered a review for the selected movie before
            cur.execute("SELECT * FROM reviews WHERE movie_id = %s AND user_id = %s", (movie_id, session["id"]))
            old = cur.fetchone()
            if old:
               flash("Your Already added you review", "message")
               return redirect(url_for("index")) 

             # Add user's review  
            cur.execute("INSERT INTO reviews (movie_id, user_id, review_text) VALUES (%s, %s, %s)", (movie_id, session["id"], review))
            mysql.connection.commit()
            cur.close()
            flash("Your Review added successfully", "message")
            return redirect(request.referrer)
        except:
            flash("Something went wrong, Try again", "message")
            return redirect(request.referrer)


# Route for getting reviews      
@app.route("/reviews")
def reviews():
    id = request.args.get("id")
    movie = request.args.get("movie")
    cur = mysql.connection.cursor()
    cur.execute("SELECT review_text,user_id, users.username FROM reviews JOIN users on reviews.user_id = users.id WHERE reviews.movie_id = %s ",(id,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("reviews.html", reviews=reviews,movie = movie )


# Route for getting suggestions
@app.route("/suggestions")
def suggest():
    movies = get_suggestions()
    return render_template("suggestions.html",movies = movies)


# Route for adding suggestions
@app.route("/suggest-add")
def suggestions_search():
    suggested = request.args.get("suggested")
    suggested_movies = get_suggestions()
    if suggested:
        # Check if suggested movie already exists on the website
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM movies WHERE movies.name =%s ",(suggested,))
        movie = cur.fetchone()
        if movie:
            flash("This Movie already exist in the website", "message")
            return redirect(request.referrer)
        for movie in suggested_movies:
            # Check if the suggested movie has been previously suggested
            if suggested.lower() == movie.lower() :
                flash("This Movie alrady suggested by other user, Thank you ")
                return redirect(request.referrer)
        append_suggestion(suggested)
        flash("Your suggestion added successfully, Thank you ")
        return redirect(request.referrer)
    

