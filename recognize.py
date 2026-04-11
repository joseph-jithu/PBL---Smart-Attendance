import face_recognition
import cv2
import pickle
import datetime
import numpy as np

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_ids = data["ids"]

# 🔥 ID → Name mapping
names = {
    "1": "Joseph(40)",
    "5":"Rishi(29)",
    "6":"Atharva(39)",
    "7":"Arihant(38)",
    "8":"sir(00)",
    "9":"Anuj(37)",
    "10":"Sarvesh(41)",
    "11":"Shriya(23)"
    
    
}

# Start camera
cap = cv2.VideoCapture(0)

marked = set()

print("Press ESC to exit...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert BGR → RGB
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = face_recognition.face_locations(rgb)

    # Encode faces
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), encoding in zip(faces, encodings):

        # Scale back to original size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        matches = face_recognition.compare_faces(known_encodings, encoding)
        distances = face_recognition.face_distance(known_encodings, encoding)

        name = "Unknown"

        if len(distances) > 0:
            best_match_index = np.argmin(distances)

            if matches[best_match_index]:
                id = known_ids[best_match_index]
                name = names.get(id, "Unknown")

                # Mark attendance once
                if name not in marked:
                    with open("attendance.csv", "a") as f:
                        now = datetime.datetime.now()
                        f.write(f"{name},{now}\n")
                    marked.add(name)

        # Draw rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Put name
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 255), 2)

    cv2.imshow("Smart Attendance System", frame)

    # 🔥 FIXED EXIT (ESC key)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

# Release camera properly
cap.release()
cv2.destroyAllWindows()
