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

cursor.execute("""CREATE TABLE bugs (id integer, status integer, title text, description text, psw text)""")
con.commit()
print("Configuration of bugs' database is ended. The database name is ", settings["database"])