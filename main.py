import time
import csv
import cv2
import face_recognition
import os
from datetime import datetime, timedelta

import users_record
import face


def capture_face():
    known_face_encodings, known_face_names = face.load()  # Load known faces
    records = users_record.load()  # Load user records from CSV
    video_capture = cv2.VideoCapture(0)  # Open the webcam

    while True:
        ret, frame = video_capture.read()  # Capture frame-by-frame
        rgb_frame = frame[:, :, ::-1]  # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)  # Check if the face exists
            if any(matches):
                index = matches.index(True)
                name = known_face_names[index]

                last_time = records.get(name)  # Check last recognition time from CSV

                # If face recognized after set duration
                if last_time is None or datetime.now() - last_time > timedelta(minutes=2):
                    print(f"Welcome back {name}! Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    records[name] = datetime.now()  # Update user records
                    users_record.write(name, records[name])  # Write user information to CSV
                else:
                    print(f"{name} recognized again, ignoring.Time: "
                          f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                name = input("Enter the name for this face: ")  # Save the new face
                known_face_encodings.append(face_encoding)
                known_face_names.append(name)
                face.save(frame, name)

                records[name] = datetime.now()  # Update user records
                users_record.write(name, records[name])  # Write user information to CSV

        cv2.imshow('Video', frame)  # Displaying the resulting image in video frame

        time.sleep(3)  # 3sec hold for image to stabilize

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_face()
