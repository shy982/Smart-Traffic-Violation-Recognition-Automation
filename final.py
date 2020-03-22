import mysql.connector
import mycursor
from test import myfunc
mydb  = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "shyam",
    database = "testdb"
)
if __name__ == '__main__':
    x = myfunc()
    mycursor.execute("SELECT email_id FROM license WHERE vehicle_number = {x}")
    for i in mycursor:
        print(i)