# Rostos&Frases
_Projeto que, ao identificar um rosto, mostra frases com base na sua posição._

## Objetivo:
Criar um programa que:
* Ao identificar um rosto, mostre frases;
    * aleatórias?
* Manter a frase alinhada ao rosto identificada (na parte superior);
    * Redimensionar a frase quando o rosto de afastar.
* Mudar a frase quando o rosto de aproximar e se afastar;
* Capturar o rosto (após a permissão) e construir um mosaico de rostos;
    * Com ou sem frases?
    * Redimensionar o mosaico a cada rosto inserido ou preencher um de tamanho fixo?
    * Repetir rostos?

## Andamento:

Inicialmente usamos as bibliotecas:
Nesse projeto, as seguintes bibliotecas estão sendo usadas:

* **cv2** (OpenCV): É uma biblioteca para processamento de imagem e visão computacional;

* **dlib**: Uma biblioteca que inclui recursos para detecção facial e pontos-chave (landmarks).

* **numpy**: Amplamente usada para computação numérica em Python.

Também estávamos usando um modelo já treinado para fazer o reconhecimento facial:
```python
dlib.shape_predictor
```

Tivemos avanços e bons resultados, no entanto, encontramos uma alternativa mais interessante, um recurso da `Google`.

Agora estamos dando seguimento ao projeto usando [**MediaPipe**](https://developers.google.com/mediapipe/solutions/vision/face_detector)

## ToDo:
* ~~Usar o Face detection ao invés do Face Landmark;~~
    * será usado o Face Landmark pela distância que mantêm o rosto identificado.
* ~~Fixar as frases no rosto identificado;~~
* Arrumar a velocidade das frases;
* ~~Arrumar a posição das frases;~~
* ~~Arrumar a direção das frases;~~
* Desenvolver o redimensionamento das frases com o deslocamento do rosto em Z (aumentar quando se afastar para conseguir ler);
* Mudar a frase com o deslocamento em Z;
* Fazer um mosaico com os rostos;