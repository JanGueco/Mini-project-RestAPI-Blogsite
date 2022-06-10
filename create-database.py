import mysql.connector
from getpass import getpass
import sys


username = input("Database username: ")
password_db = getpass("Database password: ")



try:
    mydb = mysql.connector.connect(
      host="localhost",
      user=username,
      password=password_db
    )
except:
    sys.exit("Credentials are inconsisent")
    
database_name = input("Database name(leave empty to use default(mytestdb): ")

if database_name == "":
    database_name = "mytestdb"


mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

existing = False
for x in mycursor:
    if database_name in x:
        print("Database existing")
        existing = True
        break

if not existing:
    mycursor.execute("CREATE DATABASE {}".format(database_name))               
    print("Database creation successful")
