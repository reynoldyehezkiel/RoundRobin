import mysql.connector

# connecting to the mysql server
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd=""
)

# cursor object c
c = db.cursor()

# executing the create database statement
c.execute("CREATE DATABASE roundrobin")

# fetching all the databases
c.execute("SHOW DATABASES")

# printing all the databases
for i in c:
	print(i)
c = db.cursor()

# finally closing the database connection
db.close()
