from flask import Flask, abort
import os
from database import configure_database,mysql
from flask import render_template, url_for, request, redirect, flash, session
from logic import append_suggestion,get_suggestions
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import math
app = Flask(__name__)

# Define the folder to store the uploaded images
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'your-secret-key' 
configure_database(app)


# Route for the home page
@app.route("/")
def index():
    cur = mysql.connection.cursor()

    # Getting query params
    category = request.args.get('type')  
    date = request.args.get('latest')  
    year = request.args.get("year")  
    name = request.args.get("movie-name") 

    # Pagination information 
    page = request.args.get('page',1 ,type=int)
    per_page = 8
    start = (page - 1)*per_page
    end = start + per_page

    # Retrieving movies according to query params
    if category:
        # Retrieve movies based on the specified category
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE categories.name = %s GROUP BY movies.id", (category,))
        movies = cur.fetchall()
    elif date:
        # Retrieve movies based on the latest release date
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.release_date >= '2023-01-01'  GROUP BY movies.id")
        movies = cur.fetchall()
    elif year and name:
        # Retrieve movies based on the specified year and movie name
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE YEAR(movies.release_date) = %s AND movies.name LIKE %s  GROUP BY movies.id",(year,'%' + name +'%'))
        movies = cur.fetchall()
    elif name:
        # Retrieve movies based on the specified movie name
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE movies.name LIKE %s  GROUP BY movies.id",('%' + name +'%',))
        movies = cur.fetchall()
    elif year:
        # Retrieve movies based on the specified year
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE  YEAR(movies.release_date) = %s GROUP BY movies.id",(year,))
        movies = cur.fetchall()
    else:
        # Retrieve all movies
        cur.execute("SELECT movies.*, categories.name, AVG(ratings.rating),YEAR(movies.release_date) FROM movies JOIN categories ON movies.category_id = categories.id LEFT JOIN ratings ON movies.id = ratings.movie_id GROUP BY movies.id")
        movies = cur.fetchall()

    # Retrieve all categories
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.close()
    # Get total pages depending on number of movies
    total_pages = math.ceil((len(movies) / per_page))
    if total_pages == 0:
        total_pages = 1
    # Specify movies for page
    movies_on_page = movies[start:end]
    # Add active class to the navigation based on the query parameters
    if category:
        return render_template("index.html", movies=movies, categories=categories, active='category', type=category,total_pages=total_pages,page=page)
    elif date:
        return render_template("index.html", movies=movies, categories=categories, active='latest',total_pages=total_pages,page=page)
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
            if user.isAdmin:
                session['admin'] = True
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
            # Call the static method to allow user to register
            success, message = User.register(username, email, password)
            if success:
                flash(message, "message")
                return redirect(url_for("login"))
            else:
                flash(message, "message")
                return redirect(url_for("register"))

        except:
            flash("An error occurred. Please try again.", "message")
            return redirect(url_for("register"))

    return render_template("register.html")

# Route for the logout page
@app.route('/logout/')
def logout():
    session['logged_in'] = False
    session['admin'] = False
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
            
            # Check if user entered empty field
            if not review.strip():
                flash("The review was empty, Try again", "message")
                return redirect(request.referrer)    
            
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
@app.route("/suggest-add",methods=["GET","POST"])
def add_suggestion():
    suggested = request.form["suggested"]
    suggested_movies = get_suggestions()
    if suggested:
    
        # check if field is empty
        if not suggested.strip():
            flash("The field was empty, Try again", "message")
            return redirect(request.referrer)
        
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

# Route for admin panel (adding-movie)     
@app.route("/admin")
def admin_panel():
    if session.get('admin') != None and session.get('admin') != False:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
        cur.close()
        return render_template("add-movie.html",categories=categories)
    else:
        abort(403, "Access to this resource is forbidden")

# Route for saving movie to DB 
@app.route("/movies/add", methods=['POST'])
def add_movie():
        try:
            # save image in images folder and get image path
            if 'image' in request.files:
                image = request.files['image']
                if image.filename != '':
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                    image_path = os.path.join('images', filename).split("\\")[1]
            
            # get form data 
            movie_name = request.form['name']
            movie_category = request.form['category_id']
            movie_date = request.form['release_date']
            movie_image = image_path
            
            #insert movie into DB
            cur = mysql.connection.cursor()
            cur.execute ("INSERT INTO movies (name, release_date, category_id, image_path) VALUES (%s, %s, %s, %s)", (movie_name, movie_date, movie_category, movie_image))
            mysql.connection.commit()
            cur.close()
            
            flash('Movie added successfully to the website', "message")
            return redirect(url_for('index'))
        except:
            flash('Error happened, Try to add the movie again', "message")
            return redirect(request.referrer)



