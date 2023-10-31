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

def get_text_and_color(distance, i, marca_prox, marca_dist):
    colors = [(0, 255, 0), (0, 255, 255), (0, 0, 255)]  # Verde, Amarelo, Vermelho
    phrases = [
        ["Ola, estou aqui para ajudar!", "Registro: Pessoa comum", "Intruso detectado: A maquina observa."],
        ["Tenha um otimo dia!", "Registro: Sujeito nao identificado", "Nas sombras ciberneticas, estamos te vigiando."],
        ["Voce e muito especial para nos.", "Registro: Visitante desconhecido", "A tecnologia nunca fecha os olhos."],
        ["Sinto muito, nao posso fazer isso.", "Registro: Entidade digital", "Seus movimentos sao agora digitais."],
        ["Estamos aqui para apoia-lo.", "Registro: Ser humano autenticado", "Cameras roboticas te seguem como sombras implacaveis."],
        ["Por favor, forneça mais informacoes.", "Registro: Identidade nao verificada", "Voce e agora parte de nossa opera digital."],
        ["Tudo ficara bem.", "Registro: Presenca detectada", "Seu rosto e apenas um pixel na tela do desconhecido."],
        ["Voce e valioso para nos.", "Registro: Visitante nao autorizado", "As sombras do ciberespaco sussurram."],
        ["Obrigado por escolher nossos servicos.", "Registro: Usuario comum", "O DNA digital da humanidade se desenrola."],
        ["Nao consigo responder a essa pergunta.", "Registro: Consulta anonima", "Aqui, somos todos prisioneiros da Matrix."],
        ["Voce e unico de sua maneira.", "Registro: Entidade desconhecida", "Nossas vidas sao tracadas na areia do tempo."],
        ["Estou aqui para ajudar.", "Registro: Identidade nao verificada", "O olho eletronico nao pode ser enganado."],
        ["Como voce esta hoje?", "Registro: Pessoa sem identificacao", "Sua presenca digital e uma linha de codigo."],
        ["Vamos encontrar uma solucao.", "Registro: Ser humano autenticado", "As sombras ciberneticas escondem segredos."],
        ["Voce e especial para nos.", "Registro: Visitante nao autorizado", "Cada clique e um passo mais fundo na toca do coelho."],
        ["Sinta-se a vontade para perguntar.", "Registro: Identidade desconhecida", "As redes invisiveis tecem nosso destino digital."],
        ["Desculpe, nao compreendi.", "Registro: Consulta nao identificada", "A presenca humana e apenas um traco de pixels."],
        ["Estamos aqui para ajudar.", "Registro: Entidade digital", "A memoria da maquina nunca se desvanece com o tempo."],
        ["Como posso te auxiliar?", "Registro: Pessoa comum", "Cada acao e uma gota no oceano da ciber-realidade."],
        ["O que voce gostaria de fazer?", "Registro: Identidade nao verificada", "Nossa existencia e uma linha de codigo em constante evolucao."],
        ["Vamos resolver isso juntos.", "Registro: Ser humano autenticado", "Aqui, a privacidade e uma ilusao fugaz e efemera."],
        ["Sua opiniao e importante para nos.", "Registro: Visitante desconhecido", "Os observadores ciberneticos veem o invisivel."],
        ["Estamos prontos para ajudar.", "Registro: Identidade nao verificada", "Somos marionetes nas maos do mestre da tecnologia."],
        ["Como posso ser util?", "Registro: Pessoa sem identificacao", "O registro digital e o testemunho de nossa jornada."],
        ["Ficarei feliz em te auxiliar.", "Registro: Visitante nao autorizado", "A vigilancia e o preco que pagamos pela conveniencia."],
        ["Em que posso te ajudar hoje?", "Registro: Consulta anonima", "O olho da maquina e onipresente e onisciente."],
        ["Voce e importante para nos.", "Registro: Identidade nao verificada", "As redes invisiveis tecem nosso destino digital."],
        ["Como posso te apoiar?", "Registro: Ser humano autenticado", "Nossas vidas sao tracadas na areia do tempo cibernetico."],
        ["Sinta-se a vontade para perguntar.", "Registro: Pessoa sem identificacao", "A memoria da maquina e eterna e intransigente."],
        ["Estou a disposicao.", "Registro: Identidade desconhecida", "Os segredos digitais estao escondidos nas entrelinhas."],
        ["O que voce precisa?", "Registro: Consulta nao identificada", "Cada acao e uma gota no oceano da ciber-realidade."],
        ["Vamos encontrar uma solucao juntos.", "Registro: Visitante desconhecido", "Nossa existencia e uma linha de codigo em constante evolucao."],
        ["Voce e unico.", "Registro: Entidade digital", "Aqui, a privacidade e uma ilusao fugaz e efemera."],
        ["O que posso fazer por voce?", "Registro: Identidade nao verificada", "Os observadores ciberneticos veem o invisivel."],
        ["Como posso ser de auxilio?", "Registro: Pessoa comum", "Somos marionetes nas maos do mestre da tecnologia."],
        ["Estou aqui para te ajudar.", "Registro: Ser humano autenticado", "O registro digital e o testemunho de nossa jornada."],
        ["Como posso ser util hoje?", "Registro: Visitante nao autorizado", "A vigilancia e o preco que pagamos pela conveniencia."],
        ["Em que posso te auxiliar hoje?", "Registro: Consulta anonima", "O olho da maquina e onipresente e onisciente."],
        ["Voce e valioso para nos.", "Registro: Identidade nao verificada", "As redes invisiveis tecem nosso destino digital."],
        ["Como posso te apoiar?", "Registro: Ser humano autenticado", "Nossas vidas sao tracadas na areia do tempo cibernetico."],
        ["Sinta-se a vontade para perguntar.", "Registro: Pessoa sem identificacao", "A memoria da maquina e eterna e intransigente."],
        ["Estou a disposicao.", "Registro: Identidade desconhecida", "Os segredos digitais estao escondidos nas entrelinhas."],
        ["O que voce precisa?", "Registro: Consulta nao identificada", "Cada acao e uma gota no oceano da ciber-realidade."],
        ["Vamos encontrar uma solucao juntos.", "Registro: Visitante desconhecido", "Nossa existencia e uma linha de codigo em constante evolucao."],
        ["Voce e unico.", "Registro: Entidade digital", "Aqui, a privacidade e uma ilusao fugaz e efemera."],
        ["O que posso fazer por voce?", "Registro: Identidade nao verificada", "Os observadores ciberneticos veem o invisivel."],
        ["Como posso ser de auxilio?", "Registro: Pessoa comum", "Somos marionetes nas maos do mestre da tecnologia."],
        ["Estou aqui para te ajudar.", "Registro: Ser humano autenticado", "O registro digital e o testemunho de nossa jornada."],
        ["Como posso ser util hoje?", "Registro: Visitante nao autorizado", "A vigilancia e o preco que pagamos pela conveniencia."],
        ["Em que posso te auxiliar hoje?", "Registro: Consulta anonima", "O olho da maquina e onipresente e onisciente."],
        ["Voce e valioso para nos.", "Registro: Identidade nao verificada", "As redes invisiveis tecem nosso destino digital."],
        ["Como posso te apoiar?", "Registro: Ser humano autenticado", "Nossas vidas sao tracadas na areia do tempo cibernetico."],
        ["Sinta-se a vontade para perguntar.", "Registro: Pessoa sem identificacao", "A memoria da maquina e eterna e intransigente."],
        ["Estou a disposicao.", "Registro: Identidade desconhecida", "Os segredos digitais estao escondidos nas entrelinhas."],
        ["O que voce precisa?", "Registro: Consulta nao identificada", "Cada acao e uma gota no oceano da ciber-realidade."],
        ["Vamos encontrar uma solucao juntos.", "Registro: Visitante desconhecido", "Nossa existencia e uma linha de codigo em constante evolucao."],
        ["Voce e unico.", "Registro: Entidade digital", "Aqui, a privacidade e uma ilusao fugaz e efemera."],
        ["O que posso fazer por voce?", "Registro: Identidade nao verificada", "Os observadores ciberneticos veem o invisivel."],
        ["Como posso ser de auxilio?", "Registro: Pessoa comum", "Somos marionetes nas maos do mestre da tecnologia."],
        ["Estou aqui para te ajudar.", "Registro: Ser humano autenticado", "O registro digital e o testemunho de nossa jornada."],
        ["Como posso ser util hoje?", "Registro: Visitante nao autorizado", "A vigilancia e o preco que pagamos pela conveniencia."],
        ["Em que posso te auxiliar hoje?", "Registro: Consulta anonima", "O olho da maquina e onipresente e onisciente."],
        ["Voce e valioso para nos.", "Registro: Identidade nao verificada", "As redes invisiveis tecem nosso destino digital."],
        ["Como posso te apoiar?", "Registro: Ser humano autenticado", "Nossas vidas sao tracadas na areia do tempo cibernetico."],
        ["Sinta-se a vontade para perguntar.", "Registro: Pessoa sem identificacao", "A memoria da maquina e eterna e intransigente."],
        ["Estou a disposicao.", "Registro: Identidade desconhecida", "Os segredos digitais estao escondidos nas entrelinhas."],
        ["O que voce precisa?", "Registro: Consulta nao identificada", "Cada acao e uma gota no oceano da ciber-realidade."],
        ["Vamos encontrar uma solucao juntos.", "Registro: Visitante desconhecido", "Nossa existencia e uma linha de codigo em constante evolucao."],
        ["Voce e unico.", "Registro: Entidade digital", "Aqui, a privacidade e uma ilusao fugaz e efemera."],
        ["O que posso fazer por voce?", "Registro: Identidade nao verificada", "Os observadores ciberneticos veem o invisivel."],
        ["Como posso ser de auxilio?", "Registro: Pessoa comum", "Somos marionetes nas maos do mestre da tecnologia."],
        ["Estou aqui para te ajudar.", "Registro: Ser humano autenticado", "O registro digital e o testemunho de nossa jornada."],
        ["Como posso ser util hoje?", "Registro: Visitante nao autorizado", "A vigilancia e o preco que pagamos pela conveniencia."],
        ["Em que posso te auxiliar hoje?", "Registro: Consulta anonima", "O olho da maquina e onipresente e onisciente."],
        ["Voce e valioso para nos.", "Registro: Identidade nao verificada", "As redes invisiveis tecem nosso destino digital."],
        ["Como posso te apoiar?", "Registro: Ser humano autenticado", "Nossas vidas sao tracadas na areia do tempo cibernetico."]
    ]

    if distance > marca_prox:
        phrase = phrases[i][0]
        color = colors[0]  # Verde
    elif distance < marca_prox and distance > marca_dist:
        phrase = phrases[i][1]
        color = colors[1]  # Amarelo
    elif distance < marca_dist:
        phrase = phrases[i][2]
        color = colors[2]  # Vermelho

    return phrase, color

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

def make_landmarks(mp_drawing, mp_face_mesh, mp_drawing_styles, image, face_landmarks):
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_tesselation_style())
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_IRISES,
        landmark_drawing_spec=None,         
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_iris_connections_style())
    
def is_face_near_edge(x_forehead, y_forehead, x_chin, y_chin, image_shape, margin=50):
    # Obtém as dimensões da imagem
    height, width = image_shape

    # Verifica se o rosto está muito próximo da borda da imagem com a margem especificada
    if (
        x_forehead < margin
        or y_forehead < margin
        or width - x_chin < margin
        or height - y_chin < margin
    ):
        return True
    else:
        return False