import cv2
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

user_id = input("Enter user ID: ")

cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        count += 1
        
        # Save image
        file_path = f"dataset/User.{user_id}.{count}.jpg"
        cv2.imwrite(file_path, gray[y:y+h, x:x+w])
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow("Capturing Faces", frame)
    
    if cv2.waitKey(1) == 27 or count >= 30:
        break

cap.release()
cv2.destroyAllWindows()