"""
Face Recognition Attendance System
Main entry point - Run this file to start the attendance system
"""

import cv2
import face_recognition
import numpy as np
import os
import csv
import pickle
from datetime import datetime
from utils.encoder import load_encodings
from utils.attendance import mark_attendance, get_today_attendance


def run_attendance():
    """Main function to run the attendance system using webcam."""
    
    print("\n" + "="*50)
    print("   FACE RECOGNITION ATTENDANCE SYSTEM")
    print("="*50)

    # Load known face encodings
    encodings_path = "models/encodings.pkl"
    if not os.path.exists(encodings_path):
        print("\n[ERROR] No face encodings found!")
        print("Please run: python register_faces.py  (to register students first)")
        return

    print("\n[INFO] Loading face encodings...")
    known_encodings, known_names = load_encodings(encodings_path)
    print(f"[INFO] Loaded {len(known_names)} registered face(s): {', '.join(set(known_names))}")

    # Start webcam
    print("\n[INFO] Starting webcam... Press 'Q' to quit.")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Check your camera connection.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    marked_today = set(get_today_attendance())
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read from webcam.")
            break

        frame_count += 1

        # Process every 3rd frame for performance
        if frame_count % 3 == 0:
            # Resize for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces and get encodings
            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)

                name = "Unknown"
                color = (0, 0, 255)  # Red for unknown

                if len(face_distances) > 0:
                    best_match_idx = np.argmin(face_distances)
                    if matches[best_match_idx]:
                        name = known_names[best_match_idx]
                        color = (0, 255, 0)  # Green for known

                        # Mark attendance
                        if name not in marked_today:
                            mark_attendance(name)
                            marked_today.add(name)
                            print(f"[✔] Attendance marked: {name} at {datetime.now().strftime('%H:%M:%S')}")

                # Scale back up face locations
                top, right, bottom, left = [v * 4 for v in face_location]

                # Draw rectangle and label
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)

                label = name if name == "Unknown" else f"{name} ✔" if name in marked_today else name
                cv2.putText(frame, label, (left + 5, bottom - 8),
                            cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        # UI overlay
        date_str = datetime.now().strftime("%d %b %Y  |  %H:%M:%S")
        cv2.putText(frame, date_str, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"Marked Today: {len(marked_today)}", (10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, "Press Q to quit", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Face Recognition Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n[INFO] Attendance session ended.")
    print(f"[INFO] Attendance saved to: attendance/{datetime.now().strftime('%Y-%m-%d')}_attendance.csv")


if __name__ == "__main__":
    run_attendance()
