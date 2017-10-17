import numpy as np
import cv2
import sqlite3
face_detect = cv2.CascadeClassifier('D:/ANACONDA3/envs/venv1/Library/etc/haarcascades/haarcascade_frontalface_default.xml')

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile=row
    conn.close()
    return profile

cam = cv2.VideoCapture(0)
rec = cv2.face.createLBPHFaceRecognizer(threshold=90)
rec.load("D:/python_opencv/face_rec_train/recognizer/trainningData.yml")
font=cv2.FONT_HERSHEY_PLAIN
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h)in faces:
        cv2.rectangle(img, (x,y),(x + w, y + h),(0, 255, 255), 2)
        id = rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if profile!=None:
            cv2.putText(img, str(profile[1]), (x, y + h + 30), font, 2,(255, 255, 0), 2)
            cv2.putText(img, str(profile[2]), (x, y + h + 60), font, 2, (255, 255, 0), 2)
            cv2.putText(img, str(profile[3]), (x, y + h + 90), font, 2, (255, 255, 0), 2)

    cv2.imshow("Face",img)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()