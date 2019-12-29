import os
import psycopg2

# Connect to database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Open a cursor to perform database operations
cur = conn.cursor()

# Query database and pass in data, safe from SQL injections
cur.execute("SELECT * FROM transactions WHERE catid = %i);", (5))

# Another way
sql = "SELECT * FROM transactions WHERE catid = %i);"
data = (5)
cur.execute(sql, data)

# Obtain queried data as a Python object
result = cur.fetchone()

# If changing the database, make the changes persistent
# conn.commit()

# Close communication with the database
cur.close()
conn.close()
