import time
import csv
import cv2
import face_recognition
import os
from datetime import datetime, timedelta


def save_face(face_encoding, name):
    if not os.path.exists("known_faces"):  # Create a directory to store face images if not exists
        os.makedirs("known_faces")

    filename = f"known_faces/{name}.jpg"
    cv2.imwrite(filename, face_encoding)
    print("Face saved successfully!")


# Function to load known faces and their encodings
def load_faces():
    known_face_encodings = []
    known_face_names = []

    if os.path.exists("known_faces"):  # Check if the directory exists
        for filename in os.listdir("known_faces"):
            if filename.endswith('.jpg'):
                name = os.path.splitext(filename)[0]
                image = face_recognition.load_image_file(f"known_faces/{filename}")
                encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(encoding)
                known_face_names.append(name)

    return known_face_encodings, known_face_names


def load_user_records():
    user_records = {}
    if os.path.exists("user_records.csv"):
        with open('user_records.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                user_records[row[0]] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    return user_records


# Function to write user information to CSV
def write_to_csv(name, login_time):
    with open('user_records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, login_time.strftime('%Y-%m-%d %H:%M:%S')])


def capture_face():
    known_face_encodings, known_face_names = load_faces()  # Load known faces
    user_records = load_user_records()  # Load user records from CSV
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

                last_time = user_records.get(name)  # Check last recognition time from CSV

                # If face recognized after set duration
                if last_time is None or datetime.now() - last_time > timedelta(minutes=2):
                    print(f"Welcome back {name}! Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    user_records[name] = datetime.now()  # Update user records
                    write_to_csv(name, user_records[name])  # Write user information to CSV
                else:
                    print(f"{name} recognized again within 8 hours, ignoring.Time: "
                          f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                name = input("Enter the name for this face: ")  # Save the new face
                known_face_encodings.append(face_encoding)
                known_face_names.append(name)
                save_face(frame, name)

                user_records[name] = datetime.now()  # Update user records
                write_to_csv(name, user_records[name])  # Write user information to CSV

        cv2.imshow('Video', frame)  # Displaying the resulting image in video frame

        time.sleep(3)  # 3sec hold for image to stabilize

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_face()
