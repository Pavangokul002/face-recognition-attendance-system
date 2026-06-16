"""
Face Registration Script
Run this FIRST to register student/employee faces before using the attendance system.

Usage:
    python register_faces.py

This script will:
1. Ask for the person's name
2. Open the webcam
3. Capture 30 face samples automatically
4. Save the face encodings to models/encodings.pkl
"""

import cv2
import face_recognition
import os
import pickle
import numpy as np
from datetime import datetime


DATASET_DIR = "dataset"
ENCODINGS_PATH = "models/encodings.pkl"
SAMPLES_NEEDED = 30  # Number of face samples to capture per person


def capture_faces(name: str) -> list:
    """Capture face samples from webcam for a given person."""
    
    save_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return []

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    encodings = []
    count = 0

    print(f"\n[INFO] Capturing {SAMPLES_NEEDED} face samples for '{name}'")
    print("[INFO] Look at the camera. Move your head slightly for better accuracy.")
    print("[INFO] Press 'Q' to cancel at any time.\n")

    while count < SAMPLES_NEEDED:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        display = frame.copy()

        for face_location in face_locations:
            top, right, bottom, left = face_location

            # Only process one face at a time
            if len(face_locations) == 1:
                face_encoding = face_recognition.face_encodings(rgb_frame, [face_location])
                if face_encoding:
                    encodings.append(face_encoding[0])
                    count += 1

                    # Save image sample
                    img_path = os.path.join(save_dir, f"{name}_{count}.jpg")
                    face_img = frame[top:bottom, left:right]
                    if face_img.size > 0:
                        cv2.imwrite(img_path, face_img)

                    color = (0, 255, 0)
            else:
                color = (0, 165, 255)

            cv2.rectangle(display, (left, top), (right, bottom), color, 2)

        # UI overlay
        progress = int((count / SAMPLES_NEEDED) * (display.shape[1] - 40))
        cv2.rectangle(display, (20, display.shape[0] - 35), (display.shape[1] - 20, display.shape[0] - 15), (50, 50, 50), -1)
        cv2.rectangle(display, (20, display.shape[0] - 35), (20 + progress, display.shape[0] - 15), (0, 200, 100), -1)

        status = f"Capturing: {count}/{SAMPLES_NEEDED}"
        cv2.putText(display, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(display, f"Name: {name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if len(face_locations) != 1:
            msg = "Multiple faces!" if len(face_locations) > 1 else "No face detected"
            cv2.putText(display, msg, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)

        cv2.imshow("Register Face - Press Q to cancel", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n[INFO] Registration cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return []

    cap.release()
    cv2.destroyAllWindows()
    return encodings


def save_encodings(name: str, new_encodings: list):
    """Save or update face encodings in the pickle file."""
    
    os.makedirs("models", exist_ok=True)

    known_encodings = []
    known_names = []

    # Load existing encodings
    if os.path.exists(ENCODINGS_PATH):
        with open(ENCODINGS_PATH, "rb") as f:
            data = pickle.load(f)
            known_encodings = data["encodings"]
            known_names = data["names"]

        # Remove old encodings for this person (re-registration)
        paired = [(e, n) for e, n in zip(known_encodings, known_names) if n != name]
        if paired:
            known_encodings, known_names = zip(*paired)
            known_encodings = list(known_encodings)
            known_names = list(known_names)
        else:
            known_encodings, known_names = [], []

    # Add new encodings
    known_encodings.extend(new_encodings)
    known_names.extend([name] * len(new_encodings))

    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print(f"\n[✔] Saved {len(new_encodings)} encodings for '{name}'")
    print(f"[INFO] Total registered: {len(set(known_names))} person(s)")


def list_registered():
    """Print all registered persons."""
    if not os.path.exists(ENCODINGS_PATH):
        print("\n[INFO] No registered faces found.")
        return

    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
    names = sorted(set(data["names"]))
    print(f"\n[INFO] Registered persons ({len(names)}):")
    for i, name in enumerate(names, 1):
        count = data["names"].count(name)
        print(f"  {i}. {name}  ({count} samples)")


def main():
    print("\n" + "="*50)
    print("   FACE REGISTRATION")
    print("="*50)

    while True:
        print("\nOptions:")
        print("  1. Register a new person")
        print("  2. List registered persons")
        print("  3. Exit")
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            name = input("Enter full name (e.g., John_Smith): ").strip().replace(" ", "_")
            if not name:
                print("[ERROR] Name cannot be empty.")
                continue

            encodings = capture_faces(name)
            if encodings:
                save_encodings(name, encodings)
                print(f"\n[✔] Registration complete for '{name}'!")
            else:
                print("[ERROR] No encodings captured. Try again.")

        elif choice == "2":
            list_registered()

        elif choice == "3":
            print("\n[INFO] Exiting registration.")
            break
        else:
            print("[ERROR] Invalid choice.")


if __name__ == "__main__":
    main()
