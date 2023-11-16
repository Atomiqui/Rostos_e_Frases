import os
import time
from PIL import Image, ImageDraw, UnidentifiedImageError
import cv2
import numpy as np

pasta = r'.\images'

def redimensionar_imagem(imagem, tamanho):
    return imagem.resize((tamanho, tamanho))

def criar_mosaico(imagens, tamanho_imagem):
    num_imagens = len(imagens)
    largura_mosaico = int(num_imagens ** 0.5) + 1  # Calcula o número de colunas (e também de linhas) para formar um mosaico quadrado
    altura_mosaico = largura_mosaico
    mosaico = Image.new("RGB", (largura_mosaico * tamanho_imagem, altura_mosaico * tamanho_imagem), "white")

    for i, imagem in enumerate(imagens):
        x = i % largura_mosaico
        y = i // largura_mosaico
        posicao_x = x * tamanho_imagem
        posicao_y = y * tamanho_imagem

        mosaico.paste(imagem, (posicao_x, posicao_y))

    return mosaico

while True:
    if os.path.exists(pasta):
        imagens_redimensionadas = []
        arquivos_png = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.png')]

        tamanho_imagem = 100
        for arquivo_png in arquivos_png:
            try:
                imagem = Image.open(os.path.join(pasta, arquivo_png))
            except UnidentifiedImageError:
                print(f'O arquivo {arquivo_png} não é uma imagem válida.')
                continue

            imagem_redimensionada = redimensionar_imagem(imagem, tamanho_imagem)
            imagens_redimensionadas.append(imagem_redimensionada)

        mosaico = criar_mosaico(imagens_redimensionadas, tamanho_imagem)

        # Converta o mosaico para uma matriz numpy (formato que o OpenCV pode lidar)
        mosaico_array = cv2.cvtColor(np.array(mosaico), cv2.COLOR_RGB2BGR)

        # Salve o mosaico em P:\GitHub\Labinter\Rostos_e_Frases\
        caminho_salvamento = r'.\mosaico.png'
        cv2.imwrite(caminho_salvamento, mosaico_array)

    else:
        print(f'A pasta {pasta} não existe.')

    time.sleep(1)
