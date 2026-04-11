import face_recognition
import os
import pickle

# Path to dataset
dataset_path = "dataset"

known_encodings = []
known_ids = []

print("Processing images...")

for file in os.listdir(dataset_path):
    img_path = os.path.join(dataset_path, file)

    # Load image
    image = face_recognition.load_image_file(img_path)

    # Convert to encoding
    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        encoding = encodings[0]

        # Extract ID from filename (User.1.1.jpg → 1)
        id = file.split('.')[1]

        known_encodings.append(encoding)
        known_ids.append(id)

        print(f"Encoded {file}")

# Save encodings
data = {
    "encodings": known_encodings,
    "ids": known_ids
}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Encodings saved successfully!")