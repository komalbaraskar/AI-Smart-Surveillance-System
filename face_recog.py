import face_recognition
import os

known_encodings = []
known_names = []

def load_faces():
    global known_encodings, known_names

    if not os.path.exists("faces"):
        print("No faces folder found")
        return

    for file in os.listdir("faces"):
        try:
            img = face_recognition.load_image_file(f"faces/{file}")
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(file.split(".")[0])

        except:
            print(f"Skipping {file}")

def recognize_face(frame):
    rgb = frame[:, :, ::-1]

    try:
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        names = []

        for enc in encodings:
            matches = face_recognition.compare_faces(known_encodings, enc)
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                name = known_names[idx]

            names.append(name)

        return faces, names

    except Exception as e:
        print("⚠ Face recognition error:", e)
        return [], []