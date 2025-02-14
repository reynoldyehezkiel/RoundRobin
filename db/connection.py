import mysql.connector

class Connection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            # database="roundrobin"
            database="roundrobintest"
        )
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# Use a single shared database instance
connector = Connection()
