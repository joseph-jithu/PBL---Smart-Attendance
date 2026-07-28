# Smart Attendance System

An AI-powered Smart Attendance System that automates student attendance using **Computer Vision** and **Face Recognition**. The system detects and recognizes registered students in real time through a webcam and marks attendance automatically, eliminating the need for manual attendance.

---

## Features

- Real-time face detection using OpenCV
- Face recognition using machine learning
- Automatic attendance marking
- Date and time stamping for every attendance entry
- Attendance stored in CSV format
- Fast and contactless attendance process
- Webcam-based recognition

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| OpenCV | Face Detection & Image Processing |
| face_recognition | Face Encoding & Recognition |
| NumPy | Numerical Computations |
| Pandas | Attendance Data Management |
| CSV | Attendance Storage |

---

## Project Structure

```
Smart-Attendance-System/
│
├── images/                 # Registered student images
├── Attendance.csv          # Attendance records
├── main.py                 # Main application
├── EncodeGenerator.py      # Generates face encodings
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-Attendance-System.git
```

### 2. Navigate into the Project

```bash
cd Smart-Attendance-System
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the main application:

```bash
python main.py
```

The webcam will open and start detecting registered faces. Once a face is recognized, attendance is automatically recorded.

---

## How It Works

1. Register student images.
2. Generate face encodings.
3. Start the webcam.
4. Detect faces in each frame.
5. Compare detected faces with stored encodings.
6. Identify the student.
7. Record attendance with the current date and time.
8. Prevent duplicate attendance entries for the same session.

---

## Workflow

```
Student Face
      │
      ▼
 Webcam Capture
      │
      ▼
 Face Detection
      │
      ▼
 Face Encoding
      │
      ▼
 Face Matching
      │
      ▼
 Student Identified
      │
      ▼
 Attendance Marked
```

---

## Future Improvements

- Database integration (MySQL/MongoDB)
- Web-based dashboard
- Multiple classroom support
- Live attendance analytics
- Student registration portal
- Anti-spoofing using liveness detection
- Email notifications
- Cloud deployment

---

## Learning Outcomes

Through this project, I gained experience in:

- Computer Vision fundamentals
- Face Recognition techniques
- OpenCV image processing
- Python application development
- Data handling with Pandas
- Real-time video processing
- Machine Learning integration

---

## Applications

- Schools
- Colleges
- Coaching Institutes
- Corporate Employee Attendance
- Training Centers

---

## License

This project is intended for educational and learning purposes.

---

## Author

**Joseph Jithu**

- B.Tech Information Technology
- Pune Institute of Computer Technology (PICT)

If you found this project useful, feel free to star the repository.
