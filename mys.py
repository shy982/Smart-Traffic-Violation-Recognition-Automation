import mysql.connector
mydb  = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "shyam",
    database = "testdb"
)

mycursor = mydb.cursor()
#def create_database():
#    mycursor.execute("CREATE TABLE LICENSE (name VARCHAR(255),vehicle_number VARCHAR(255),email_id VARCHAR(255))")
#    sqlFormula = "INSERT INTO license (name, vehicle_number, email_id) VALUES (%s, %s, %s)"
#
#    riders = [("Nikhil Rathaur","010 K 414","nikhilrathaur1998@yahoo.com"),
#              ("Vinayak Patil", "785 K 686", "vp120369@gmail.com"),
#              ("Shyam R","538 E 945" ,"shyam.9801.08@gmail.com"),
#              ("Harry Potter", "032 A 163", "harry@gmail.com"),
#              ("Rohan Panday", "BJ 7496","rohan2434@gmail.com"),
#              ("Shaurya Sinha" , "042 K 729","shouryan4579@gmail.com"),
#              ("Anubhav Singh", "ZD 45480","anubhav1998@gmail.com"),
#              ("Yogesh Chandra", "06 5010","yogesh7893@gmail.com"),
#              ("Lokesh SK","MCLRN F1" , "loki001@gmail.com")]
#    mycursor.executemany(sqlFormula, riders)
#    mydb.commit()
def query(test):
    x = test
    val = """SELECT email_id FROM license  WHERE vehicle_number = %s """
    mycursor.execute(val, (x,))
    mail = ""
    for i in mycursor:
        mail += str(i)
    mail_add=mail[2:-3]
    #print(mail[2:-3])
    return mail_add
mycursor.execute("ALTER TABLE license ADD phone_number varchar(15) AFTER email_id")
#if __name__ == '__main__':
#    #create_database()
#   mail=query("010 K 414")