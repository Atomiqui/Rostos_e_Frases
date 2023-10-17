import cv2
import os
import numpy as np

# Pasta onde as imagens foram salvas
images_folder = "imagens"

# Listar todas as imagens na pasta
image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder) if file.endswith(".png")]

# Verifique se há imagens para criar o mosaico
if not image_files:
    print("Nenhuma imagem encontrada para criar o mosaico.")
else:
    # Carregue todas as imagens e crie o mosaico
    images = [cv2.imread(file) for file in image_files]
    num_columns = 3
    num_rows = 3

    # Determine a largura e a altura do mosaico
    width = images[0].shape[1]
    height = images[0].shape[0]
    mosaic_width = width * num_columns
    mosaic_height = height * num_rows

    # Crie um mosaico em branco
    mosaic = 255 * np.ones(shape=[mosaic_height, mosaic_width, 3], dtype=np.uint8)

    # Preencha o mosaico com as imagens
    for i, image in enumerate(images):
        row = i // num_columns
        col = i % num_columns
        y1 = row * height
        y2 = y1 + height
        x1 = col * width
        x2 = x1 + width
        mosaic[y1:y2, x1:x2] = image

    # Salve o mosaico resultante
    cv2.imwrite("mosaico.png", mosaic)
    print(f"Mosaico criado e salvo como 'mosaico.png'.")
