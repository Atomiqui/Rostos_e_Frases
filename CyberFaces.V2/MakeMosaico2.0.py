import os
import time
from PIL import Image, ImageDraw, UnidentifiedImageError
import cv2
import numpy as np
import random
import Functionalities as func

def redimensionar_imagem(imagem, tamanho): 
    return imagem.resize((tamanho, tamanho))

def cortar_imagem_com_pontos(imagem, pontos):

    imagem_cortada = Image.new('RGBA', imagem.size, (0, 0, 0, 0))

    desenhador = ImageDraw.Draw(imagem_cortada)

    desenhador.polygon(pontos, fill=(0, 0, 0))

    imagem_cortada.paste(imagem, mask=imagem_cortada)

    #xy = random.randint(200, 800)
    return imagem_cortada.resize((350, 350))

def criar_mosaico(imagens, tamanho_imagem):
    num_imagens = len(imagens)
    largura_mosaico = 1500
    altura_mosaico = 800

    # Crie uma imagem branca com suporte a canal alfa (RGBA)
    mosaico = Image.new("RGBA", (largura_mosaico, altura_mosaico), (0, 0, 0, 0))

    posUsadas = []

    for i, imagem in enumerate(imagens):
        posicao_x = random.randint(-tamanho_imagem*1.5, largura_mosaico)
        posicao_y = random.randint(-tamanho_imagem*1.5, altura_mosaico)

        if ((posicao_x, posicao_y) not in posUsadas):
            mosaico.paste(imagem, (posicao_x, posicao_y), imagem)
            posUsadas.append((posicao_x, posicao_y))
            for j in range(100):
                posUsadas.append((posicao_x + j, posicao_y + j))
                posUsadas.append((posicao_x - j, posicao_y - j))
                posUsadas.append((posicao_x + j, posicao_y - j))
                posUsadas.append((posicao_x - j, posicao_y + j))

    return mosaico

pasta = r'.\images'

while True:
    if os.path.exists(pasta):
        imagens_redimensionadas = []
        arquivos_png = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.png')]

        vetor_coordenadas = func.load_coordenadas()

        tamanho_imagem = 50
        for arquivo_png, coordenada in zip(arquivos_png, vetor_coordenadas):
            try:
                imagem = Image.open(os.path.join(pasta, arquivo_png))
            except UnidentifiedImageError:
                print(f'O arquivo {arquivo_png} não é uma imagem válida.')
                continue

            imagemRedonda = cortar_imagem_com_pontos(imagem, coordenada)

            imagens_redimensionadas.append(imagemRedonda)
            imagemNoVetor = imagens_redimensionadas[imagens_redimensionadas.index(imagemRedonda)]

        mosaico = criar_mosaico(imagens_redimensionadas, tamanho_imagem)

        # Converta o mosaico para uma matriz numpy (formato que o OpenCV pode lidar)
        mosaico_array = cv2.cvtColor(np.array(mosaico), cv2.COLOR_RGB2BGR)

        # Salve o mosaico em P:\GitHub\Labinter\Rostos_e_Frases\
        caminho_salvamento = r'.\mosaico.png'
        cv2.imwrite(caminho_salvamento, mosaico_array)

    else:
        print(f'A pasta {pasta} não existe.')

    time.sleep(1)