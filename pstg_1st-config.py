import psycopg2
import json

settings = json.load(open("pstg_set.json", "r"))

con = psycopg2.connect(
  database=settings["database"], 
  user= settings["user"], 
  password= settings["password"], 
  host=settings["host"], 
  port=settings["port"]
)

cursor = con.cursor()
# cursor.execute("""DROP TABLE bugs""")
# con.commit()
cursor.execute("""CREATE TABLE bugs (id integer, status integer, title text, description text, email text, psw text, img text)""")
con.commit()
print("Configuration of bugs' database is ended. The database name is ", settings["database"])