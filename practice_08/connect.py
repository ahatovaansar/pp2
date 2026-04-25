import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="practice08",
    user="postgres",
    password="1234"
)

cur = conn.cursor()