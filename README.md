# Movies Review App

The Movies Review App is a web application built with Python (Flask), HTML, CSS, and JavaScript. It allows users to browse movies, add reviews and ratings, add movies to their watchlist, and suggest movies to be added to the website.

# Admin Feature: Add Movies

The Movies Review App includes an admin feature that allows authorized users to add movies to the website. To access this feature, follow these steps:

- Open the Movies Review App in your web browser.
- Log in using the admin account credentials.
  - Email: admin@gmail.com
  - Password: 123456

## Installation

To run the Movies Review App on your local machine, follow these steps:

### Prerequisites

- Python (the latest version)
- MySQL database server

### Clone the repository

```shell
git clone <repository_url>
```

### Create a virtual environment (optional but recommended)

### Install Flask and other dependencies

```bash
pip3 install Flask
pip3 install Flask-MySQL
pip3 install Werkzeug
```

### Configure the database

1. Locate the pre-exported MySQL database file (`movies.sql`) included in the project files.

2. Install MySQL if you haven't already. You can download it from the official MySQL website and follow the installation instructions for your operating system.

3. Create a new database for your application. Execute the following SQL statement:

   ```sql
   CREATE DATABASE movies;
   ```

4. Import the pre-exported database file into the movies database you just created.
5. Open the database.py file in your project and locate the following section:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movies'
```

Update the database configuration in the `server.py` file with your MySQL username and password if necessary.

### Run the application

```shell
flask --app server.py run
```
