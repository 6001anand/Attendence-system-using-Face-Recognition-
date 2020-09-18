import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

subjects = [
    "OOSE",
    "Cloud_Computing",
    "E-Commerce",
    "Internet_and_Web_Technology"
]

dicti = {
    "OOSE": 'coolanand.atre@gmail.com',
    "Cloud_Computing": "aanandatre@gmail.com",
    "E-Commerce": "tarushipatidar123@gmail.com",
    "Internet_and_Web_Technology": "tarushipatidar400@gmail.com"
}


def newStudent():

    def clear1():
        txt1.delete(0, 'end')
        #res = ""
        #message1.configure(text=res)

    def clear2():
        txt2.delete(0, 'end')
        #res = ""
        #message1.configure(text=res)

    def takeimage():
        Id = (txt1.get())
        name = (txt2.get())
        if(Id.isnumeric() and name.isalpha()):
            cam = cv2.VideoCapture(0)
            face_haar_cascade = cv2.CascadeClassifier('haas/haarcascade_frontalface_default.xml')
            sampleNum = 0
            while(True):
                ret, img = cam.read()
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_haar_cascade.detectMultiScale(gray_img, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.' +str(sampleNum) + ".jpeg", gray_img[y:y+h, x:x+w])
                    # cv2.imwrite("C:/Users/HP/Downloads/face_recognition_pictures/"+name +"."+Id +'.' +str(sampleNum) + ".jpeg", gray_img[y:y+h, x:x+w])
                    cv2.imshow('frame', img)
                if(cv2.waitKey(100) & 0xFF == ord('q')):
                    break
                elif(sampleNum > 60):
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Image saved for Id : "+ Id +", Name : "+ name
            row = [Id, name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message1.configure(text=res)
        else:
            if(Id.isnumeric()):
                res = "Enter Alphabetical Name"
                message1.configure(text=res)
            elif(name.isalpha()):
                res = "Enter Numeric ID"
                message1.configure(text=res)
            else:
                res = "Enter Numeric ID and\nAlphabetical Name"
                message1.configure(text=res)

    def trainimage():
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_haar_cascade = cv2.CascadeClassifier('haas/haarcascade_frontalface_default.xml')
        faces, Id = getImageandLabel("TrainingImage")
        face_recognizer.train(faces, np.array(Id))
        face_recognizer.save("TrainingImageLabel\Trainner.yml")
        res = "Image Trained"
        message1.configure(text=res)

    def getImageandLabel(path):
        imagePath = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imgpath in imagePath:
            pilimage = Image.open(imgpath).convert('L')
            imagenp = np.array(pilimage, 'uint8')
            Id = int(os.path.split(imgpath)[-1].split(".")[1])
            faces.append(imagenp)
            Ids.append(Id)
        return faces, Ids

    window = tk.Toplevel()
    window.title("Face Recognition")
    window.geometry('1366x768')
    window.configure(background='darkseagreen')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    back = tk.Button(window, text="Back", command=window.destroy, bg="silver", fg='black', activebackground="chocolate" ,width=5, height=1, font=('times', 15, 'bold'))
    back.place(x=0, y=0)

    message = tk.Label(window, text="Attendance System Using Face Recognition\n(Add New Student)", bg="darkslategray", fg='White', width=50, height=3, font=('times', 30, 'italic bold underline'))
    message.place(x=100, y=15)

    lb1 = tk.Label(window, text="Enter Roll No", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb1.place(x=200, y=200)

    txt1 = tk.Entry(window, width=20, fg="Black", bg='White', font=('times', 25, 'bold'))
    txt1.place(x=550, y=200)

    lb2 = tk.Label(window, text="Enter Name", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb2.place(x=200, y=300)

    txt2 = tk.Entry(window, width=20, fg="Black", bg='White', font=('times', 25, 'bold'))
    txt2.place(x=550, y=300)

    lb3 = tk.Label(window, text="Message", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb3.place(x=200, y=600)

    message1 = tk.Label(window, text="", bg="White", fg='black',activebackground="white", width=58, height=2, font=('times', 15, 'bold'))
    message1.place(x=550, y=600)

    clearbutton = tk.Button(window, text="Clear", command=clear1, bg="silver", fg='black', activebackground="silver", width=7, height=1, font=('times', 15, 'bold'))
    clearbutton.place(x=950, y=200)
    clearbutton2 = tk.Button(window, text="Clear", command=clear2, bg="silver", fg='black', activebackground="silver", width=7, height=1, font=('times', 15, 'bold'))
    clearbutton2.place(x=950, y=300)
    Quit = tk.Button(window, text="Quit", command=root.destroy, bg="silver", fg='black', activebackground="chocolate", width=7, height=1, font=('times', 15, 'bold'))
    Quit.place(x=950, y=450)

    takeimg = tk.Button(window, text="Take Picture", command=takeimage, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
    takeimg.place(x=550, y=400)
    trainimg = tk.Button(window, text="Train The Model", command=trainimage, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
    trainimg.place(x=550, y=500)


def takeAttendance():
    def send_mail(filename, sub, todaysdate):
        email_user = '6001anand.atre@gmail.com'
        email_password = "ahwjfkdewaoydkmj"
        email_send = dicti[sub]
        subject = 'Attendance System'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Hi there, sending this email for '+sub+' subject on '+todaysdate+'!'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()

    def trackImage():
        subject = variable.get()
        mail = CheckVar1.get()
        if(subject != 'Select One' and mail == 1):
            face_recognizer = cv2.face_LBPHFaceRecognizer.create()
            face_recognizer.read("TrainingImageLabel\Trainner.yml")
            face_haar_cascade = cv2.CascadeClassifier('haas/haarcascade_frontalface_default.xml')
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            colname = ['Id', 'Name'] # , 'Date', 'Time']
            Attendance = pd.DataFrame(columns=colname)
            while True:
                ret, img = cam.read()
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_haar_cascade.detectMultiScale(gray_img, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    Id, conf = face_recognizer.predict(gray_img[y:y+h, x:x+w])
                    #print(conf)
                    if conf < 35:
                        #ts = time.time()
                        #date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        # timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = df.loc[df['Id'] == Id]['Name'].values
                        aa = str(aa)
                        aa = aa[2:len(aa)-2]
                        tt = str(Id)+"-"+aa
                        Attendance.loc[len(Attendance)] = [Id, aa]# , date, timestamp]
                    else:
                        Id = 'Unknown'
                        tt = str(Id)
                    cv2.putText(img, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
                Attendance = Attendance.drop_duplicates(subset=['Id'], keep='first')
                cv2.imshow('img', img)
                if(cv2.waitKey(1) == ord('q')):
                    break
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            H, M, S = timestamp.split(":")
            filename = "Attendence\Attendence_"+subject+"_"+date+"_"+H+"-"+M+"-"+S+".csv"
            #filename = "Attendence\Attendence_"+subject+"_"+date+".csv"
            Attendance.to_csv(filename, index=False)
        
            res = Attendance['Name'].count()
            message4.configure(text=res)
            cam.release()
            cv2.destroyAllWindows()
            res = Attendance
            message2.configure(text=res)

            #if(mail == 1):
            try:
                send_mail(filename, subject, date)
                res = "The E-mail has been sent"
                message3.configure(text=res)
            except Exception as e:
                res = "Error in sending E-mail"
                message3.configure(text=res)
                print(e)
            # else:
            #      res = "Please Select check box for Email"
            #      message3.configure(text=res)

        else:

            if(subject != 'Select One'):
                res = ""
                message2.configure(text=res)
                
                res = "Please Select check box for Email"
                message3.configure(text=res)
                pass
            elif(mail == 1):
                res = "Please select subject area"
                message2.configure(text=res)
                
                res = ""
                message3.configure(text=res)
                pass
            else:
                res = "Please select subject area"
                message2.configure(text=res)
                res = "Please Select check box for Email"
                message3.configure(text=res)
                pass

    window2 = tk.Toplevel()
    window2.title("Face Recognition")
    window2.geometry('1366x768')
    window2.configure(background='darkseagreen')
    window2.grid_rowconfigure(0, weight=1)
    window2.grid_columnconfigure(0, weight=1)

    back = tk.Button(window2, text="Back", command=window2.destroy, bg="silver", fg='black', activebackground="chocolate", width=5, height=1, font=('times', 15, 'bold'))
    back.place(x=0, y=0)

    message = tk.Label(window2, text="Attendance System Using Face Recognition\n(Take Attendance)", bg="darkslategray", fg='White', width=50, height=3, font=('times', 30, 'italic bold underline'))
    message.place(x=100, y=15)
    

    lbl5 = tk.Label(window2, text="Select The Subject", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lbl5.place(x=200, y=200)

    variable = tk.StringVar(window2)
    variable.set("Select One")

    w = tk.OptionMenu(window2, variable, *subjects)
    w.config(width=73, height=2)
    w.place(x=550, y=200)

    CheckVar1 = tk.IntVar()
    C1 = tk.Checkbutton(window2, text="Send Email", variable=CheckVar1, onvalue=1, offvalue=0, height=2, width=8)
    C1.place(x=1125, y=200)

    lb4 = tk.Label(window2, text="Attendance Status", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb4.place(x=200, y=400)
    lb4 = tk.Label(window2, text="E-mail Status", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb4.place(x=200, y=500)
    lb4 = tk.Label(window2, text="Number of Student Present", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb4.place(x=200, y=600)

    message2 = tk.Label(window2, text="", bg="White", fg='black', activebackground="White", width=58, height=2, font=('times', 15, 'bold'))
    message2.place(x=550, y=400)
    message3 = tk.Label(window2, text="", bg="White", fg='black', activebackground="White", width=58, height=2, font=('times', 15, 'bold'))
    message3.place(x=550, y=500)
    message4 = tk.Label(window2, text="", bg="White", fg='black', activebackground="White", width=40, height=2, font=('times', 15, 'bold'))
    message4.place(x=550, y=600)

    trackimg = tk.Button(window2, text="Take Attendance", command=trackImage, bg="silver", fg='black', activebackground="silver" , width=20, height=2, font=('times', 15, 'bold'))
    trackimg.place(x=550, y=300)
    Quit = tk.Button(window2, text="Quit", command=root.destroy, bg="silver", fg='black', activebackground="chocolate", width=7, height=1, font=('times', 15, 'bold'))
    Quit.place(x=1125, y=600)


root = tk.Tk()
root.title("Face Recognition")
root.geometry('1366x768')
dialog_title = 'Quit'
dialog_text = 'Are you Sure'
root.configure(background='darkseagreen')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

message = tk.Label(root, text="Shri Govindram Seksaria Institute of Technology and Science", bg="darkslategray", fg='White', width=50, height=2, font=('times', 30, 'italic bold underline'))
message.place(x=100, y=15)


message1 = tk.Label(root, text="Attendance System Using Face Recognition", bg="darkslategray", fg='White', width=50, height=2, font=('times', 30, 'italic bold underline'))
message1.place(x=100, y=100)


newStu = tk.Button(root, text="Add New Student", command=newStudent, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
newStu.place(x=150, y=350)
takeAttendance = tk.Button(root, text="Take Attendance", command=takeAttendance, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
takeAttendance.place(x=950, y=350)
Quit = tk.Button(root, text="Quit", command=root.destroy, bg="silver", fg='black', activebackground="chocolate", width=10, height=1, font=('times', 15, 'bold'))
Quit.place(x=600, y=500)

root.mainloop()