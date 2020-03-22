import smtplib
from twilio.rest import Client
import numpy as np
import random
import cv2
import imutils
import pytesseract
import pandas as pd
import time
import mysql.connector
mydb  = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "vinayak",
    database = "testdb"
)

mycursor = mydb.cursor()
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
def msg_query(test):
    x = test
    val = """SELECT phone_number FROM license WHERE vehicle_number = %s """
    mycursor.execute(val,(x,))
    num = ""
    for i in mycursor:
        num+=str(i)
    phone_num = num[2:-3]
    return phone_num
def myfunc(r):
    name = ["P6070013","P6070012","P6070007","P1010005"] #sample images size
    even_day = ["Monday","Wednesday","Friday","Sunday"]
    odd_day = ["Tuesday","Thursday","Saturday"]
    cur_day = "Tuesday"
    #image = cv2.imread('P6070013.jpg') #vinayak #785 K 686
    image = cv2.imread(name[r]+'.jpg') #shyam  #538 E 945
#    image = cv2.imread('P6070007.jpg') #shubham #977 K 593
#    image = cv2.imread('P1010005.jpg') #nikhil   #010 K 414

    image = imutils.resize(image, width=500)

#    cv2.imshow("Original Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("1 - Grayscale Conversion", gray)

    gray = cv2.bilateralFilter(gray, 11, 17, 17)
# gray = cv2.GaussianBlur(gray,255,255)
#cv2.imshow("2 - Bilateral Filter", gray)
#gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,17)
    cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY ,41,3)
    edged = cv2.Canny(gray, 170, 200) #EdDeA
#cv2.imshow("4 - Canny Edges", edged)

    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #All contours irr, rect comes with 4 points
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] 
    NumberPlateCnt = None 

    #count = 0
    for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True) #approx one poly with another poly
            if len(approx) == 4:  
                NumberPlateCnt = approx 
                break
            
    # Masking the part other than the number plate
    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
    new_image = cv2.bitwise_and(image,image,mask=mask)
#    cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
#    cv2.imshow("Final_image",new_image)
            
    # Configuration for tesseract
    #config = ('-l eng --oem 3 --psm 6')
    #config = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Run tesseract OCR on image
    text = pytesseract.image_to_string(new_image, config=config)
    #Data is stored in a CSV file
    raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
                         'v_number': [text]}
            
    df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
    df.to_csv('data.csv')
    
    #if(text == "HR25D05551"):
    #    text = "HR26DQ0551"
    #elif(text == "HH1ZDE1A33"):
    #    text = "MH12DE1433"
    #elif(text == "KIL12M50218"):
    #    text = "KA 12N 5048"
#           print(text)
#           print(int(text[-1:]))
    print("The LICENSE PLATE number is " + text)
    if ((int(text[-1:])%2 == 0 and cur_day in even_day) or (int(text[-1:])%2 != 0 and cur_day in odd_day)):
        return ""
    else:
        return text
    cv2.waitKey(0)

def sendmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('shubham3962@gmail.com','nATIONAL12')
    server.sendmail('shubham3962@gmail.com',to,content)
    server.close()

def send_msg(tom):
    account_sid = 'AC0aee33b35d39b3feb0d98c2262a955b8'
    auth_token = 'b77569c4298ff5c1c83ccec72da08360'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
                body='You violated odd even rule.',
                from_='+14804093877',
                to= tom
        )
    print(message.sid)
if __name__ == '__main__':
       
    try:
        content = "You have violated the odd - even rule."
        subject = "Traffic Rule Violation"
        message = 'Subject: {}\n\n{}'.format(subject, content)
#        to = "shyam.9201.08@gmail.com"'
        r = random.randint(1,4)
        print("The Traffic Level on the road is")
        print(r)
        if(r>2):
            print("Heavy Traffic")
        else:
            print("Light Traffic")
        for i in range(0,r):
            x = myfunc(i)
            if x == "":
                print("No violation, Mail not sent")
            else:
                to_mail = query(x)
                to_msg = msg_query(x)
                send_msg(to_msg)
                sendmail(to_mail,message)
                print("Email has been sent to the defaulter")
    except Exception as e:
        print(e)
        print("Sorry email has not been sent")

