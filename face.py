import os
import cv2
import face_recognition


def save(face_encoding, name):
    if not os.path.exists("known_faces"):  # Create a directory to store face images if not exists
        os.makedirs("known_faces")

    filename = f"known_faces/{name}.jpg"
    cv2.imwrite(filename, face_encoding)
    print("Face saved successfully!")


# Function to load known faces and their encodings
def load():
    known_face_encodings = []
    known_face_names = []

    if os.path.exists("known_faces"):  # Check if the directory exists
        for filename in os.listdir("known_faces"):
            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                continue

            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(f"known_faces/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

    return known_face_encodings, known_face_names
