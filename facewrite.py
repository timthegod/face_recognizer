import numpy as np
import cv2
import sqlite3
cap = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier('D:/ANACONDA3/envs/venv1/Library/etc/haarcascades/haarcascade_frontalface_default.xml')


def insertOrUpdate(Id,Name,Age,Gender):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist==1:
        cmd="UPDATE People SET Name="+str(Name)+","+"Age="+str(Age)+","+"Gender="+str(Gender)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People (ID,Name,Age,Gender) Values("+str(Id)+","+str(Name)+","+str(Age)+","+str(Gender)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

id = input('Enter user id : ')
name = input('Enter your name : ')
age = input('Enter your age : ')
gender = input('Enter yor gender (M / F) : ')
insertOrUpdate(id,name,age,gender)
samplenum = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h)in faces:
        samplenum+=1
        cv2.imwrite("dataSet/User." + str(id)+"."+str(samplenum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(frame, (x,y),(x + w, y + h),(0, 0, 255), 2)
        cv2.waitKey(100)
    cv2.flip(frame,1,frame)
    cv2.imshow("Face",frame)
    if samplenum >=20:
        break
cap.release()
cv2.destroyAllWindows()