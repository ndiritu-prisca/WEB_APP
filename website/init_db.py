import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, email, contact, password) VALUES (?, ?, ?, ?)",
            ('Property Owner', 'property.owner@gmail.com', 712345678, 'property')
            )

connection.commit()
connection.close()