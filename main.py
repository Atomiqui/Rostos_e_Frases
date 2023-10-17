import cv2
import mediapipe as mp
import random

def get_positions(face_landmarks):
    pt_forehead = 10  # Ponto da testa
    pt_chin = 152  # Ponto do queixo

    x_forehead = face_landmarks.landmark[pt_forehead].x * image.shape[1]
    y_forehead = face_landmarks.landmark[pt_forehead].y * image.shape[0]
    x_chin = face_landmarks.landmark[pt_chin].x * image.shape[1]
    y_chin = face_landmarks.landmark[pt_chin].y * image.shape[0]

    distance = ((x_forehead - x_chin)**2 + (y_forehead - y_chin)**2)**0.5

    return distance, x_forehead, y_forehead, x_chin, y_chin

def set_text_position(x_forehead, y_forehead, frase):
    # ToDo: Definir qual string vai ficar aqui. A string deve ser centralizada no rosto
    x = int(x_forehead) - frase.__len__() * 8
    y = int(y_forehead) - 50

    return x, y

def get_text(distance, i):

    frases = [
        ['frase11', 'frase12', 'frase13'],
        ['frase21', 'frase22', 'frase23'],
        ['frase31', 'frase32', 'frase33']
    ]

    if distance > marca_prox:
        frase = frases[i][0]
    elif distance < marca_prox and distance > marca_dist:
        frase = frases[i][1]
    elif distance < marca_dist:
        frase = frases[i][2]

    return frase

mp_drawing = mp.solutions.drawing_utils
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

                distance, x_forehead, y_forehead, x_chin, y_chin = get_positions(face_landmarks)

                frase = get_text(distance, i)

                x, y = set_text_position(x_forehead, y_forehead, frase)
                
                cv2.putText(image, frase, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, "Se você aceita o uso da sua imagem para nosso Mosaico, pressione espaço!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            face_detected = True

        cv2.imshow('MediaPipe FaceMesh', image)
        
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break
        elif key == 32:  # Código da tecla de espaço
            # Recorte a área do rosto

            x1, y1 = int(x_forehead - distance), int(y_forehead - distance/2)
            x2, y2 = int(x_chin + distance), int(y_chin + distance/2)
            face_roi = image_copy[y1:y2, x1:x2]

            # Salve a área recortada do rosto como uma imagem separada
            if face_roi.shape[0] > 0 and face_roi.shape[1] > 0:
                cv2.imwrite('.\images\image' + str(cont) + '.png', face_roi)
                cont += 1

cap.release()