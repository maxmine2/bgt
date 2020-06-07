import psycopg2
import json
# from pstg_set import settings

settings = json.load(open("pstg_set.json", "r"))

con = psycopg2.connect(
  database=settings["database"], 
  user= settings["user"], 
  password= settings["password"], 
  host=settings["host"], 
  port=settings["port"]
)
cursor = con.cursor()

print("Database opened successfully")

def get_all_bugs():
  cursor.execute("SELECT * FROM bugs")
  return cursor.fetchall()

def get_bug_by_id(bug_id):
  cursor.execute("""SELECT * FROM bugs WHERE id = """ + str(bug_id))
  return cursor.fetchall()

def create_new_bug(data):
  con.rollback()
  cursor.execute("""SELECT MAX(id) FROM bugs""")
  a = cursor.fetchall()
  if a[0][0] != None:
    new_id = a[0][0] + 1
  else:
    new_id = 0
  cursor.execute("""INSERT INTO bugs VALUES (""" + str(new_id) + ", 0, '" + data["t"] + "', '" + data["d"] + "', '" + data["m"] + "', '" + data["p"] + "')")
  con.commit()
  return new_id

def change_status(bug_id, new_status):
  cursor.execute("""UPDATE bugs SET status = """ + str(new_status) + """WHERE id = """ + str(bug_id))
  con.commit()

def delete_bug(bug_id):
  cursor.execute("""DELETE FROM bugs WHERE id = """ + str(bug_id))
  con.commit()

def cancel_bug(bug_id):
  cursor.execute("""UPDATE bugs SET status = 4 WHERE id = """ + str(bug_id))
  con.commit()
