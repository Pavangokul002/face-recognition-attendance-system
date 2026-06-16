# 🎓 Face Recognition Attendance System

An automated attendance system using facial recognition — built with Python, OpenCV, and `face_recognition` library. Just look at the camera and attendance is marked instantly.

---

## 📁 Project Structure

```
face_attendance/
│
├── attendance_system.py     ← MAIN: Run this to mark attendance via webcam
├── register_faces.py        ← STEP 1: Register student/employee faces
├── view_attendance.py       ← View & export attendance reports
├── requirements.txt         ← Python dependencies
│
├── utils/
│   ├── __init__.py
│   ├── attendance.py        ← CSV read/write helpers
│   └── encoder.py           ← Face encoding loader
│
├── dataset/                 ← Auto-created: stores face image samples
│   └── John_Smith/
│       ├── John_Smith_1.jpg
│       └── ...
│
├── models/
│   └── encodings.pkl        ← Auto-created: saved face encodings
│
├── attendance/              ← Auto-created: daily CSV attendance files
│   └── 2025-06-15_attendance.csv
│
└── logs/                    ← Reserved for future logging
```

---

## 🛠️ Installation

### Step 1 — Prerequisites

Make sure you have **Python 3.8+** and a working **webcam**.

> **Windows users**: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) before installing dlib.
> **Linux users**: Run `sudo apt-get install build-essential cmake`
> **macOS users**: Run `brew install cmake`

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ `dlib` and `face_recognition` can take a few minutes to install. This is normal.

---

## 🚀 How to Use

### Step 1: Register Faces (Do this first!)

```bash
python register_faces.py
```

- Enter the person's name (e.g., `John_Smith`)
- Look at the webcam — it will auto-capture **30 face samples**
- Move your head slightly left/right for better accuracy
- Repeat for each student/employee

### Step 2: Run the Attendance System

```bash
python attendance_system.py
```

- The webcam opens and scans for faces in real time
- Recognized faces are shown with a **green box** and name
- Unknown faces are shown with a **red box**
- Attendance is saved to `attendance/YYYY-MM-DD_attendance.csv`
- Press **Q** to quit

### Step 3: View Attendance Reports

```bash
# Today's attendance
python view_attendance.py

# A specific date
python view_attendance.py 2025-06-15

# List all recorded dates
python view_attendance.py --all
```

---

## 📊 Attendance CSV Format

Each day's attendance is saved as:

```
attendance/2025-06-15_attendance.csv
```

```csv
Name,Date,Time,Status
John_Smith,2025-06-15,09:02:34,Present
Jane_Doe,2025-06-15,09:05:11,Present
```

---

## ⚙️ Configuration

You can adjust these values in `register_faces.py` and `attendance_system.py`:

| Setting | File | Default | Description |
|---|---|---|---|
| `SAMPLES_NEEDED` | `register_faces.py` | `30` | Face samples per person |
| `tolerance` | `attendance_system.py` | `0.5` | Face match strictness (lower = stricter) |
| Frame skip | `attendance_system.py` | Every 3rd frame | Adjust for CPU performance |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `dlib` install fails | Install cmake and Visual Studio Build Tools first |
| Webcam not opening | Check camera index: change `VideoCapture(0)` to `VideoCapture(1)` |
| Face not recognized | Re-register with better lighting; lower tolerance to `0.6` |
| Multiple faces detected | Only one face visible during registration |
| Slow performance | Reduce camera resolution in the script |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| `opencv-python` | Webcam capture & display |
| `face_recognition` | Face detection & encoding |
| `dlib` | Underlying ML for face_recognition |
| `numpy` | Numerical operations |

---

## 📝 Notes

- Each person should be registered in **good lighting** for best accuracy
- The system only marks attendance **once per person per day**
- Re-running `register_faces.py` with the same name **replaces** old data
- The `dataset/` folder contains raw face images; you can delete them after registration to save space (the `models/encodings.pkl` is what matters)

---

## 🤝 License

Free to use for educational and personal projects.
