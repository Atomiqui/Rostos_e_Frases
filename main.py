import cv2
import mediapipe as mp
import random
import Functionalities as func

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Não foi possível abrir a câmera.")
    else:
        cap.set(3, 4096)  # Largura da captura
        cap.set(4, 4096)  # Altura da captura
except Exception as e:
    print(f"Erro ao abrir a câmera: {e}")

# Transformar em constantes
marca_prox = 120
marca_dist = 70

i = random.randint(0, 2)
face_detected = False
image_folder = "images"
image_copy = None
with open("cont.txt", "r") as file:
    cont = int(file.read().strip())
face_info = [None, None, None]

with mp_face_mesh.FaceMesh(
    max_num_faces=3,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.4) as face_mesh:

    cv2.namedWindow('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        try:
            success, image = cap.read()

            if not success:
                break

            if image_copy is None:
                image_copy = image.copy()

            image.flags.writeable = False
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            image.flags.writeable = True

            if results.multi_face_landmarks:
                image_copy = image.copy()

                resultados = []

                for i in reversed(results.multi_face_landmarks):
                    resultados.append(i)
                
                for idx, face_landmarks in enumerate(resultados):
                    distance, x_forehead, y_forehead, x_chin, y_chin = func.get_positions(face_landmarks, image)

                    try:
                        if face_info[idx] == None:
                            i = random.randint(0, 20)
                            face_detected = True
                        else:
                            i = face_info[idx]['i']
                    except:
                        i = random.randint(0, 20)
                        face_detected = True
                    
                    frase, color, font_size = func.get_text_and_color(distance, i, marca_prox, marca_dist)
                    x, y = func.set_text_position(x_forehead, y_forehead, frase, font_size)

                    # Armazene as informações do rosto atual
                    face_info[idx] = {
                        'distance': distance,
                        'x_forehead': x_forehead,
                        'y_forehead': y_forehead,
                        'x_chin': x_chin,
                        'y_chin': y_chin,
                        'frase': frase,
                        'color': color,
                        'font_size': font_size,
                        'x_text': x,
                        'y_text': y,
                        'i': i,
                        'landmarks': face_landmarks
                    }
                    if face_detected and cont is not None:
                        func.get_rosto(face_info[idx]['distance'], face_info[idx]['x_forehead'], face_info[idx]['y_forehead'], face_info[idx]['x_chin'], face_info[idx]['y_chin'], image_copy, cont)
                        cont += 1
                        face_detected = False

                for i in range(3):
                    if i > idx:
                        face_info[i] = None

                for info in face_info:
                    if info:
                        func.make_landmarks(mp_drawing, mp_face_mesh, mp_drawing_styles, image, info['landmarks'])
                        cv2.putText(image, info['frase'], (info['x_text'], info['y_text']), cv2.FONT_HERSHEY_SIMPLEX, info['font_size'], info['color'], 2, cv2.LINE_AA)
            else:
                face_detected = False
                face_info = [None, None, None]

            cv2.imshow('MediaPipe FaceMesh', image)
            
            key = cv2.waitKey(5) & 0xFF
            if key == 27:
                break

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
        
cap.release()
cv2.destroyAllWindows()
with open("cont.txt", "w") as file:
    file.write(str(cont))