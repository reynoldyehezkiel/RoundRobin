import mysql.connector

# connecting to the mysql server
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="roundrobin"
)

c = db.cursor()