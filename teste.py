import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)


with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.4) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            break
        
        image.flags.writeable = False
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.flags.writeable = True

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    print(landmark)
                    print(landmark.x)
                    print(landmark.y)
                    print(landmark.z)
                    print(landmark.visibility)
                    print("\n")