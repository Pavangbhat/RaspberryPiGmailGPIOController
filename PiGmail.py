"""
**************************************************************************************************************************************
THE FOLLOWING CODE ALLOWS YOU TO CONTROL GPIO PINS(HIGH OR LOW) THROUGH THE SUBJECT OF GAMIL
THINGS TO BE TAKEN CARE OF:
                        #SUBJECT OF MAIL,MUST CONTAIN ONLY PINNUMBER(BCM) AND PINSIGNAL WITH A SPACE INBETWEEN
                                 *********
                                 *EX:14 1*
                                 *   14 0*
                                 *********
                        #CHARACTERS IN SUBJECT WOULD END THE SCRIPT
                        #FOR MORE TAKE A LOOK ON README
**************************************************************************************************************************************
"""
from imaplib import IMAP4_SSL
from email import message_from_bytes #requires python3
import RPi.GPIO as GPIO
from sys import exit

#SETTING pin numbering system as BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def High(PinNumber):
   GPIO.setup(PinNumber, GPIO.OUT)
   GPIO.output(PinNumber, 1)

def Low(PinNumber):
    GPIO.setup(PinNumber, GPIO.OUT)
    GPIO.output(PinNumber, 0)

mail = IMAP4_SSL('imap.gmail.com')  # connects IMAP services
mail.login("YourMailId@gmail.com", "password")

while True:
    # print(mail.list())
    mail.select("INBOX")
    result, data = mail.search(None,"ALL")  # first item of list which contains all mail as [b'1 2 3 4'],#result is string as "ok"(status)
    ids = data[0]  # ids will be b'1 2 3 4'
    # print(ids)#output b'1 2 3 4'
    id_list = ids.split()  # eleliminates space and makes a new list
    # print(id_list) [b'1', b'2', b'3', b'4'
    latest_id = id_list[-1]
    # print(latest_id)

    result, data = mail.fetch(latest_id, "(RFC822)")  # "RFC822" REFERS TO EMAIL BODY
    # result is string as "ok"(status) if extra variable is not used then data would be a tuple with a string and raw mail
    # print(result,data)[(b'58 (RFC822 {4719}', b'Delivered-To:....
    raw_email = data[0][1]  # the data is big list which contains first element as tuple which contains all info
    raw_email_split = raw_email.split()  # raw_mail is of type <class bytes>
    # print(raw_email_split)#raw_mail is of type <class bytes>

    email_message = message_from_bytes(raw_email)  # email parser
    Subject = email_message["subject"]  # subject as string
    SubjectList = Subject.split()  # eleliminates spaces in a string and make them into a list
    try:
        PinNumber = int(SubjectList[0])  # converting string to a number
        PinSignal = int(SubjectList[1])
    except:
        mail.logout()
        print("LOGGED OUT")
        exit(0)


    if PinSignal == 0:
        Low(PinNumber)
    else:
        High(PinNumber)


