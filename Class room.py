import cv2
import numpy as np
import face_recognition
from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('localhost:27017')
db = client['attendance']
students_col = db['students']
attendance_col = db['attendance']

# Retrieve data from the students collection
students = students_col.find()
1
# Create lists of known face encodings and names
known_face_encodings = []
known_face_names = []

for student in students:
    # Load the student's image and encode their face
    image = cv2.imread(student['image_path'])
    encoding = face_recognition.face_encodings(image)[0]

    # Add the encoding and name to the lists
    known_face_encodings.append(encoding)
    known_face_names.append(student['name'])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Start the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame from the webcam
    ret, frame = video_capture.read()

    # Resize the frame to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition. face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found, retrieve the student's name from the database and add it to the list of names
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                attendance_col.insert_one({'student_name': name})

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video',frame)
    cv2.waitKey(1)
