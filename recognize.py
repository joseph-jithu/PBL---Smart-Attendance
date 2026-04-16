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

# ID → Name mapping
names = {
    "1": "Joseph",
    "5": "Rishi",
    "6": "Atharva",
    "7": "Arihant",
    "8": "sir"
}

# Start camera (1 = external webcam, 0 = laptop camera)
cap = cv2.VideoCapture(0)

# 🔥 Increase resolution (important for multiple faces)
cap.set(3, 1920)   # width
cap.set(4, 1080)   # height

# 🔥 Fullscreen window
cv2.namedWindow("Smart Attendance System", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Smart Attendance System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

marked = set()

print("Press ESC to exit...")

# 🔥 Accuracy threshold
threshold = 0.5

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Resize for faster processing (but still good quality)
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

    # Convert BGR → RGB
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces (use CNN for better accuracy if system supports)
    faces = face_recognition.face_locations(rgb)

    # Encode faces
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), encoding in zip(faces, encodings):

        # Scale back coordinates
        top = int(top / 0.75)
        right = int(right / 0.75)
        bottom = int(bottom / 0.75)
        left = int(left / 0.75)

        distances = face_recognition.face_distance(known_encodings, encoding)

        name = "Unknown"

        if len(distances) > 0:
            best_match_index = np.argmin(distances)

            # 🔥 Use threshold instead of boolean match
            if distances[best_match_index] < threshold:
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

        # Confidence score
        if len(distances) > 0:
            confidence = 1 - distances[best_match_index]
            label = f"{name} ({confidence:.2f})"
        else:
            label = name

        # Put name
        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 255), 2)

    # 🔥 Show number of faces detected
    cv2.putText(frame, f"Faces: {len(faces)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    # ESC to exit
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release camera
cap.release()
cv2.destroyAllWindows()
