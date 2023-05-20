# Ai-Class-Room-monitoring
The  code is an example of a Python script for face recognition-based attendance tracking using the OpenCV and face_recognition libraries. It assumes that you have a MongoDB database set up to store student information and attendance records. Here's a sample of the code that is made by me :

1. Import the required libraries: The script imports the necessary libraries, including `cv2` for video capture and image processing, `numpy` for numerical operations, `face_recognition` for face detection and recognition, and `pymongo` for connecting to the MongoDB database.

2. Connect to the MongoDB database: The script establishes a connection to the MongoDB database and initializes the required collections.

3. Retrieve student data: It fetches the student data from the MongoDB collection `students`.

4. Encode known faces: The script iterates over the student data, loads each student's image, and encodes their face using the `face_recognition` library. The face encodings and corresponding names are stored in separate lists.

5. Initialize variables and start the webcam: Various variables are initialized, including face locations, encodings, and names. The script then starts capturing video from the webcam using `cv2.VideoCapture`.

6. Process video frames: Inside the main loop, each frame from the webcam is captured and resized for faster processing. The frame is converted from BGR to RGB format to be compatible with the `face_recognition` library.

7. Face detection and recognition: Every other frame is processed to save computational resources. The script detects face locations and encodes them using `face_recognition.face_locations` and `face_recognition.face_encodings` functions. It then compares the detected face encodings with the known face encodings using `face_recognition.compare_faces` to determine if there's a match.

8. Update attendance records: If a match is found, the student's name is retrieved based on the index of the first matching encoding. The student's name is then inserted into the `attendance` collection of the MongoDB database.

9. Display results: The script overlays rectangles around the detected faces and displays the corresponding names on the video frame using `cv2.rectangle` and `cv2.putText`. The resulting image is displayed using `cv2.imshow`.

10. Terminate the program: The script waits for a key press using `cv2.waitKey(1)`. Pressing any key will terminate the program and close the video window.

