import mysql.connector

mydb  = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "shyam",
    database = "testdb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE LICENSE (name VARCHAR(255),vehicle_number VARCHAR(255),email_id VARCHAR(255))")

sqlFormula = "INSERT INTO license (name, vehicle_number, email_id) VALUES (%s, %s, %s)"

riders = [("Nikhil Rathaur","010 K 414","nikhilrathaur1998@yahoo.com"),
          ("Vinayak Patil", "785 K 686", "vp120369@gmail.com"),
          ("Shyam R","538 E 945" ,"shyam.9201.08@gmail.com"),
          ("Shubham Kumar","977 K 593" ,"shubham7070078010@gmail.com"),
          ("Harry Potter", "032 A 163", "harry@gmail.com"),
          ("Rohan Panday", "BJ 7496","rohan2434@gmail.com"),
          ("Shaurya Sinha" , "042 K 729","shouryan4579@gmail.com"),
          ("Anubhav Singh", "ZD 45480","anubhav1998@gmail.com"),
          ("Yogesh Chandra", "06 5010","yogesh7893@gmail.com"),
          ("Lokesh SK","MCLRN F1" , "loki001@gmail.com")]
mycursor.executemany(sqlFormula, riders)
mydb.commit()
