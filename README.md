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

## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  - Module name: os
- [x] It contains at least one class written by you that has both properties and methods.
  - File name for the class definition: models/user.py
  - Line number(s) for the class definition:5
  - Name of two properties: id, username
  - Name of two methods: find_by_email_and_password, register (used in register route in server.py file, line 120).
  - File name and line numbers where the methods are used: models/user.py line 13, line 25.
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript.
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements.
  - File name: server.py
  - Line number(s): 38 ,109
- [x] It contains loops.
  - File name: static/scripts/watch-list.js
  - Line number(s): 17
- [x] It lets the user enter a value in a text box at some point.
      This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
