🎓 Face Recognition Attendance System

An automated attendance system that uses real-time facial recognition 
to detect and mark attendance via webcam — no manual entry needed.

Built with Python | OpenCV | face_recognition | dlib | NumPy

Features:
- Real-time face detection and recognition via webcam
- Auto-marks attendance once per day per person
- Saves records to CSV (Name, Date, Time, Status)
- Register unlimited faces via webcam
- View and export attendance reports by date
- Lightweight and runs on any standard laptop webcam

How to run:
1. pip install -r requirements.txt
2. python register_faces.py   ← register faces first
3. python attendance_system.py ← start attendance
4. python view_attendance.py   ← view reports
