import psycopg2
from pstg_set import settings

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








get_all_bugs()