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
    "8": "sir",
    "9": "Anuj",
    "10": "Sarvesh",
    "11": "Shriya"
}

# Start camera
cap = cv2.VideoCapture(2)

# 🔥 Reduce buffer lag (important for mobile cam)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 🔥 Use lower resolution for speed
cap.set(3, 640)
cap.set(4, 480)

# Fullscreen window
cv2.namedWindow("Smart Attendance System", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Smart Attendance System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

marked = set()
print("Press ESC to exit...")

threshold = 0.5
frame_count = 0
results = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # 🔥 Resize early (faster processing)
    frame = cv2.resize(frame, (640, 480))

    frame_count += 1

    # 🔥 Process every 3rd frame only
    if frame_count % 3 == 0:

        # Smaller frame for detection
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # 🔥 Faster model (HOG)
        faces = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, faces)

        results = []

        for (top, right, bottom, left), encoding in zip(faces, encodings):

            # Scale coordinates back
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            distances = face_recognition.face_distance(known_encodings, encoding)

            name = "Unknown"
            confidence = 0

            if len(distances) > 0:
                best_match_index = np.argmin(distances)

                if distances[best_match_index] < threshold:
                    id = known_ids[best_match_index]
                    name = names.get(id, "Unknown")
                    confidence = 1 - distances[best_match_index]

                    # Mark attendance once
                    if name not in marked:
                        with open("attendance.csv", "a") as f:
                            now = datetime.datetime.now()
                            f.write(f"{name},{now}\n")
                        marked.add(name)

            results.append((top, right, bottom, left, name, confidence))

    # 🔥 Draw results every frame (smooth display)
    for (top, right, bottom, left, name, confidence) in results:

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        label = f"{name} ({confidence:.2f})" if name != "Unknown" else name

        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

    # Show face count
    cv2.putText(frame, f"Faces: {len(results)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
