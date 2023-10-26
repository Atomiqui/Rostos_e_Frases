import os
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np

# Função para carregar todas as imagens na pasta
def carregar_imagens(pasta):
    imagens = []
    for root, _, files in os.walk(pasta):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                imagem = Image.open(os.path.join(root, file))
                imagens.append(imagem)
    return imagens

# Função para criar um mosaico com as imagens
def criar_mosaico(imagens):
    tamanho_mosaico = (5, 5)
    largura, altura = imagens[0].size
    largura_mosaico = largura * tamanho_mosaico[1]
    altura_mosaico = altura * tamanho_mosaico[0]

    mosaico = Image.new('RGB', (largura_mosaico, altura_mosaico), (255, 255, 255))

    for i in range(min(len(imagens), tamanho_mosaico[0] * tamanho_mosaico[1])):
        linha = i // tamanho_mosaico[1]
        coluna = i % tamanho_mosaico[1]
        mosaico.paste(imagens[i], (coluna * largura, linha * altura))

    return mosaico

# Função para atualizar o mosaico na interface gráfica
def atualizar_mosaico():
    imagens = carregar_imagens(pasta_imagens)
    mosaico = criar_mosaico(imagens)
    img_mosaico = ImageTk.PhotoImage(mosaico)

    label_mosaico.config(image=img_mosaico)
    label_mosaico.image = img_mosaico

    # Agendar a próxima atualização em 1 segundo
    janela.after(1000, atualizar_mosaico)



# Configurações da pasta de imagens
pasta_imagens = "P:\GitHub\Labinter\Rostos_e_Frases\images"

while True:
    # Verifique se a pasta existe antes de iniciar a interface gráfica
    if os.path.exists(pasta_imagens):
        # Configuração da janela gráfica
        janela = tk.Tk()
        janela.title("Mosaico de Imagens")

        # Carrega imagens e cria o mosaico inicial
        imagens = carregar_imagens(pasta_imagens)
        mosaico = criar_mosaico(imagens)
        img_mosaico = ImageTk.PhotoImage(mosaico)

        # Exibe o mosaico na interface gráfica
        label_mosaico = tk.Label(janela, image=img_mosaico)
        label_mosaico.pack()

        # Inicia a atualização automática do mosaico
        atualizar_mosaico()

        # Inicia a interface gráfica
        janela.mainloop()
