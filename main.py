import cv2
import mediapipe as mp
import random
import Functionalities as func

# mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)
cap.set(3, 4096)  # Largura da captura
cap.set(4, 4096)  # Altura da captura

# Transformar em constantes
marca_prox = 120
marca_dist = 70

i = random.randint(0, 2)
face_detected = True
image_folder = "images"
image_copy = None
cont = 0
images = []
resized_image = []

with mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    # Crie uma janela em tela cheia
    cv2.namedWindow('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            break

        if image_copy is None:
            image_copy = image.copy()

        image.flags.writeable = False
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.flags.writeable = True

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                image_copy = image.copy()

                if face_detected:
                    i = random.randint(0, 2)
                    face_detected = False

                distance, x_forehead, y_forehead, x_chin, y_chin = func.get_positions(face_landmarks, image)

                frase = func.get_text(distance, i, marca_prox, marca_dist)

                x, y = func.set_text_position(x_forehead, y_forehead, frase)
                
                cv2.putText(image, frase, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, "Se você aceita o uso da sua imagem para nosso Mosaico, pressione espaço!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            face_detected = True

        cv2.imshow('MediaPipe FaceMesh', image)
        
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break
        elif key == 32 and not face_detected:  # Código da tecla de espaço
            # Recorte a área do rosto
            cont = func.get_rosto(distance, x_forehead, y_forehead, x_chin, y_chin, image_copy, cont)
            images, resized_image = func.make_mosaico(images=images, resized_images=resized_image)

cap.release()