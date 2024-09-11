import random
import smtplib


def sendmail(receiver, subject, body):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    password = "wfpe zozr pozh ijip"
    server.login("mohamedmohamedbeirouk@gmail.com",password)
    
    message = f'subject:{subject}\n\n{body}'
    server.sendmail("mohamedmohamedbeirouk@gmail.com",receiver,message)
    server.quit()