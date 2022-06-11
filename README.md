# Project details
A simple blog app API. Users can create posts and comments.

# Installation overview

 1. Python requirements
 2. MySQL
 3. Initialization
 4. Populating the database

## Python Requirements
Modules we need:

### 1. django
   The web development framework used in this application.

 ### 2. djangorestframework
  A toolkit for django to build web APIs.

 ### 3. django-rest-knox
 A better token authentication based on django rest framework's existing token authentication.
 ### 4. mysqlclient
Used to connect to a MySQL database.
	
There's a file named *PythonRequirements.txt* that has all the requirements listed, to install open a terminal and type:
	
    pip install -r PythonRequirements.txt
  
## MySQL installation
To install MySQL:
1. Download from
  - https://www.mysql.com/downloads/
2. Install
-  https://dev.mysql.com/doc/refman/8.0/en/installing.html  (install guides)


## Initialization
Inside the root directory of the project, a python file called `create-database.py` is present. 
Use python to run the script, if no errors were raised, a database should be created.

    python create-database.py

*Note: Inputted database accounts should have priveleges.*
### `create-database.py` inputs:
1. database username
2. database password
3. desired database name

*Note: The default database name is 'mytestdb' and changing the name will require you to modify the application's settings later on.*
### Changing the default database settings of the app
From the root directory, navigate inside the *miniproject* folder and open `settings.py`.
Change the respective data about the database:

    DATABASES = {

	'default': {

	'ENGINE': 'django.db.backends.mysql',

	'NAME': 'mytestdb', #put your database name here

	'USER' : 'database_username', #put your database username here

	'PASSWORD': 'database_password', #put your database password here

	'HOST' : 'localhost',

	'PORT' : '3306',

	}

	}
    
### Migrating to the database
After defining what database should be used, we can now migrate our fields to the database.
Open a terminal inside the root directory of the project and enter:

    python manage.py migrate
The database should have all the fields registered after this command.
## Populating the database
Inside the root directory, there is a python script called `populate-database.py`
Running this script will generate *5 users, 3 posts each user, and  2 comments per post*.

*Note: The data inserted is only sample data without any real context*

# Running the server
If the data population raised no errors, the server is safe to run.
To run the server, open a terminal inside the root directory of the project and enter:

    python manage.py runserver
## API methods

 1. Sign up - `/auth/signup` **POST**
	 - Body
   `email`  - user’s email
  `password`  - user’s password
  `name`  - user’s name
 2. Log in - `/auth/login`  **POST**
	 - Body
	 `email`  - user’s email
	  `password`  - user’s password
	  
*Note: A successful login will release a token*
	
 3. Create post - `/posts` **POST**
	- Headers: - Authorization: "Bearer {token}"
	- Body
	 `title`  - blog title
	 `content`  - blog content
 4. Update post - `/posts/<post_id>` **PUT**
	 - Arguments: post_id
	 - Headers: - Authorization: "Bearer {token}"
	 - Body
	 `title`  - blog title
	 `content`  - blog content
 5. Delete post - `/posts/<post_id>` **DELETE**
	  - Headers: - Authorization: "Bearer {token}"
	  - Arguments: post_id
 7. Get all of the logged in user's post - `/me/posts` **GET**
	 - Headers: - Authorization: "Bearer {token}"
 8. Get all posts - `/posts` **GET**
 9. Get single post - `/posts/<post_id>` **GET**
	 - Arguments: post_id
 10. Create comment - `posts/<post_id>/comments` **POST**
	 - Arguments: post_id
	  - Body
	 `content`  - comment content
 11. Delete comment - `posts/<post_id>/comments/<comment_id>` **DELETE**
	 - Arguments: post_id, comment_id
	 - Headers: - Authorization: "Bearer {token}"
 12. Get comments from post - `/posts/:post_id/comments` **GET**
	  - Arguments: post_id

## Entity relationship diagram
![ERD](https://user-images.githubusercontent.com/37333940/173130628-6384bebb-d765-49f1-8f88-34dc78132389.png)
