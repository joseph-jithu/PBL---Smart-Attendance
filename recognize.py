import face_recognition
import cv2
import pickle
import datetime
import numpy as np
import mysql.connector
import face_recognition
import cv2
import pickle
import datetime
import numpy as np
import mysql.connector
import sys

# ✅ Get subject from Flask
SUBJECT = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
print("Subject received:", SUBJECT)

# ✅ Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pict12345",
    database="attendance_system"
)
cursor = db.cursor()

# ✅ Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_ids = data["ids"]

# ✅ Student mapping
students = {
    "1": {"name": "Joseph", "roll": 1},
    "5": {"name": "Rishi", "roll": 5},
    "6": {"name": "Atharva", "roll": 6},
    "7": {"name": "Arihant", "roll": 7},
    "8": {"name": "sir", "roll": 8},
    "9": {"name": "Anuj", "roll": 9},
    "10": {"name": "Sarvesh", "roll": 10},
    "11": {"name": "Shriya", "roll": 11}
}

# ✅ Use laptop camera (change index if needed)
cap = cv2.VideoCapture(1)

cap.set(3, 640)
cap.set(4, 480)

marked = set()
threshold = 0.5

print("Press ESC to exit camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    face_count = len(faces)

    for (top, right, bottom, left), encoding in zip(faces, encodings):

        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        name = "Unknown"
        confidence = 0
        roll = None

        distances = face_recognition.face_distance(known_encodings, encoding)

        if len(distances) > 0:
            best_match = np.argmin(distances)
            confidence = 1 - distances[best_match]

            if distances[best_match] < threshold:
                student_id = known_ids[best_match]
                student = students.get(student_id)

                if student:
                    name = student["name"]
                    roll = student["roll"]

                    key = f"{roll}_{SUBJECT}"

                    if key not in marked:
                        now = datetime.datetime.now()

                        cursor.execute(
                            "INSERT INTO attendance (roll_no, student_name, subject, timestamp) VALUES (%s,%s,%s,%s)",
                            (roll, name, SUBJECT, now)
                        )
                        db.commit()

                        marked.add(key)

        # ✅ Box color (Green = known, Red = unknown)
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # ✅ Label
        if name != "Unknown":
            label = f"{name} ({confidence:.2f})"
        else:
            label = "Unknown"

        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

    #  Display Subject
    cv2.putText(frame, f"Subject: {SUBJECT}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    #  Display Face Count
    cv2.putText(frame, f"Faces: {face_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
)
cursor = db.cursor()

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_ids = data["ids"]

#  ID → Name + Roll mapping (INT roll numbers)
students = {
    "1": {"name": "Joseph", "roll": 1},
    "5": {"name": "Rishi", "roll": 5},
    "6": {"name": "Atharva", "roll": 6},
    "7": {"name": "Arihant", "roll": 7},
    "8": {"name": "sir", "roll": 8},
    "9": {"name": "Anuj", "roll": 9},
    "10": {"name": "Sarvesh", "roll": 10},
    "11": {"name": "Shriya", "roll": 11}
}

#  Default laptop camera
cap = cv2.VideoCapture(1)

# Reduce lag
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(3, 640)
cap.set(4, 480)

# Fullscreen window
cv2.namedWindow("Smart Attendance System", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Smart Attendance System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

marked = set()
threshold = 0.5
frame_count = 0
results = []

print("Press ESC to exit...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))
    frame_count += 1

    #  Process every 3rd frame
    if frame_count % 3 == 0:

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, faces)

        results = []

        for (top, right, bottom, left), encoding in zip(faces, encodings):

            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            distances = face_recognition.face_distance(known_encodings, encoding)

            name = "Unknown"
            roll_no = -1
            confidence = 0

            if len(distances) > 0:
                best_match_index = np.argmin(distances)

                if distances[best_match_index] < threshold:
                    student_id = known_ids[best_match_index]
                    student = students.get(student_id, None)

                    if student:
                        name = student["name"]
                        roll_no = student["roll"]
                        confidence = 1 - distances[best_match_index]

                        #  Prevent duplicate marking (same subject session)
                        unique_key = f"{roll_no}_{SUBJECT}"

                        if unique_key not in marked:
                            now = datetime.datetime.now()

                            query = """
                            INSERT INTO attendance (roll_no, student_name, subject, timestamp)
                            VALUES (%s, %s, %s, %s)
                            """
                            values = (roll_no, name, SUBJECT, now)

                            cursor.execute(query, values)
                            db.commit()

                            marked.add(unique_key)

            results.append((top, right, bottom, left, name, confidence))

    # Draw results
    for (top, right, bottom, left, name, confidence) in results:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        label = f"{name} ({confidence:.2f})" if name != "Unknown" else name

        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

    # Display info
    cv2.putText(frame, f"Subject: {SUBJECT}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.putText(frame, f"Faces: {len(results)}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
