import cv2

import Functionalities as func
from Functionalities import face_info



mp_face_mesh = func.mp.solutions.face_mesh

# Tentativa de acesso à camera com tratamento se der erro (except)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Não foi possível abrir a câmera.")
    else:
        cap.set(3, 4096)  # Largura da captura
        cap.set(4, 4096)  # Altura da captura
except Exception as e:
    print(f"Erro ao abrir a câmera: {e}")

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
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as face_mesh:

    cv2.namedWindow('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    func.main_loop(cap, face_mesh)
        
cap.release()
cv2.destroyAllWindows()
with open("cont.txt", "w") as file:
    file.write(str(cont))