import face_recognition
import os
import pickle

dataset_path = "dataset"

#  Step 1: Load existing encodings (if available)
if os.path.exists("encodings.pkl"):
    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)
    known_encodings = data["encodings"]
    known_ids = data["ids"]
    print("Loaded existing encodings...")
else:
    known_encodings = []
    known_ids = []
    print("No existing encodings found. Starting fresh...")

#  Step 2: Load processed files list
processed_files = set()

if os.path.exists("processed.txt"):
    with open("processed.txt", "r") as f:
        processed_files = set(f.read().splitlines())

print("Already processed files:", processed_files)

#  Step 3: Process ONLY new images
new_count = 0

for file in os.listdir(dataset_path):

    # Skip if already processed
    if file in processed_files:
        continue

    img_path = os.path.join(dataset_path, file)

    # Load image
    image = face_recognition.load_image_file(img_path)

    # Get encoding
    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        encoding = encodings[0]

        # Extract ID from filename
        try:
            id = file.split('.')[1]
        except:
            print(f"Skipping invalid filename: {file}")
            continue

        # Save encoding
        known_encodings.append(encoding)
        known_ids.append(id)

        processed_files.add(file)
        new_count += 1

        print(f"Encoded NEW: {file}")

    else:
        print(f"No face found in: {file}")

#  Step 4: Save updated encodings
data = {
    "encodings": known_encodings,
    "ids": known_ids
}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

#  Step 5: Save processed file list
with open("processed.txt", "w") as f:
    for file in processed_files:
        f.write(file + "\n")

print("\n Encoding update complete!")
print(f"New images processed: {new_count}")
print(f"Total known faces: {len(known_ids)}")
