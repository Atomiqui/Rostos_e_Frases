import cv2
import os

def get_positions(face_landmarks, image):
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

def get_text(distance, i, marca_prox, marca_dist):

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

def get_rosto(distance, x_forehead, y_forehead, x_chin, y_chin, image_copy, cont):
    x1, y1 = int(x_forehead - distance), int(y_forehead - distance/2)
    x2, y2 = int(x_chin + distance), int(y_chin + distance/2)
    face_roi = image_copy[y1:y2, x1:x2]

    # Salve a área recortada do rosto como uma imagem separada
    if face_roi.shape[0] > 0 and face_roi.shape[1] > 0:
        image_folder = "images"

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            
        cv2.imwrite('.\images\image' + str(cont) + '.png', face_roi)
        return cont + 1
    
def make_mosaico(output_file="mosaico.png", mosaic_size=(1024, 1024), images = [], resized_images = []):
    image_folder = "images"

    # Verifique se a pasta de imagens existe
    if not os.path.exists(image_folder):
        print("Pasta de imagens não encontrada.")
        return

    # Obtenha uma lista de todas as imagens na pasta
    file = os.listdir(image_folder)[-1]
    if file.endswith(".png"):
        image_path = os.path.join(image_folder, file)
        image = cv2.imread(image_path)
        if image is not None:
            images.append(image)

    # Verifique se há pelo menos uma imagem
    if not images:
        print("Nenhuma imagem encontrada na pasta.")
        return
    
    # Redimensione todas as imagens para o mesmo tamanho
    image = images[-1]
    resized_image = cv2.resize(image, mosaic_size)
    resized_images.append(resized_image)

    # Crie um mosaico com as imagens
    rows, cols = int(len(resized_images) ** 0.5), int(len(resized_images) ** 0.5)
    mosaic = None

    for r in range(rows):
        row_mosaic = None
        for c in range(cols):
            idx = r * cols + c
            if idx < len(resized_images):
                if row_mosaic is None:
                    row_mosaic = resized_images[idx]
                else:
                    row_mosaic = cv2.hconcat([row_mosaic, resized_images[idx]])
        if mosaic is None:
            mosaic = row_mosaic
        else:
            mosaic = cv2.vconcat([mosaic, row_mosaic])

    # Salve o mosaico resultante em um arquivo de saída
    cv2.imwrite(output_file, mosaic)
    # print(f"Mosaico gerado e salvo em {output_file}")

    return images, resized_images