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

    cont = func.main_loop(cap, face_mesh, cont)
        
cap.release()
cv2.destroyAllWindows()
with open("cont.txt", "w") as file:
    file.write(str(cont))