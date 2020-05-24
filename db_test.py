import sqlite3
con = sqlite3.connect("flask\\bgt\\bugs.db")
cursor = con.cursor()


sql = "SELECT * FROM bugs WHERE id > -1"
cursor.execute(sql)
print(cursor.fetchall())