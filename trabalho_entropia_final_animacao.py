import math
import random
import numpy as np
import turtle
import time

# --- CONFIGURAÇÕES VISUAIS ---
n_atomos = 9      
n_movimentacoes = 2000  
VELOCIDADE = 0.07      

tamanho_tanque = 9
tamanho_ambiente = 25

direcoes = {'cima': (0, 1), 'baixo': (0, -1), 'direita': (1, 0), 'esquerda': (-1, 0)}

# Dimensões
T_LARG = int(math.sqrt(tamanho_tanque))
T_ALT = T_LARG
A_LARG = int(math.sqrt(tamanho_ambiente))
A_ALT = A_LARG

# --- SETUP TURTLE ---
CELL_SIZE = 50
GRID_SPACING = 100
OFFSET_X = -300
OFFSET_Y = -50

wn = turtle.Screen()
wn.title("Simulação Visual (Início Aleatório)")
wn.bgcolor("white")
wn.setup(width=1000, height=600)
wn.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.width(2)

atom = turtle.Turtle()
atom.hideturtle()
atom.penup()
atom.speed(0)

hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.goto(0, 200)

# --- FUNÇÕES ---
def draw_grid(start_x, start_y, rows, cols, color):
    pen.color(color)
    pen.penup()
    pen.goto(start_x, start_y)
    pen.pendown()
    for _ in range(2):                    # Desenha o quadrado maior externo
        pen.forward(cols * CELL_SIZE)
        pen.left(90)
        pen.forward(rows * CELL_SIZE)
        pen.left(90)
    pen.width(1)
    pen.color("lightgray")
    for i in range(1, cols):              # Desenha as colunas dos quadrados menores dentro do grid
        pen.penup()
        pen.goto(start_x + i * CELL_SIZE, start_y)
        pen.pendown()
        pen.goto(start_x + i * CELL_SIZE, start_y + rows * CELL_SIZE)
    for i in range(1, rows):             # Desenha as linhas dos quadrados menores dentro do grid
        pen.penup()
        pen.goto(start_x, start_y + i * CELL_SIZE)
        pen.pendown()
        pen.goto(start_x + cols * CELL_SIZE, start_y + i * CELL_SIZE)
    pen.width(2)

def render_atoms(atom_dict, base_x, base_y, color):
    atom.color(color)
    diametro = CELL_SIZE * 0.8
    for pos in atom_dict.values():
        x_fisico, y_fisico = pos
        screen_x = base_x + (x_fisico * CELL_SIZE) + (CELL_SIZE / 2)     # A pos. x na tela da animação. No centro do quadrado
        screen_y = base_y + (y_fisico * CELL_SIZE) + (CELL_SIZE / 2)     # Mesma coisa p/ o y
        atom.goto(screen_x, screen_y)
        atom.dot(diametro)                 # Desenha o círculo com diametro valendo 80% do tamanho do quadrado

# --- LAYOUT (Ambiente Esq | Tanque Dir) ---
BASE_X_AMBIENTE = -400
BASE_Y_AMBIENTE = -100
BASE_X_TANQUE = BASE_X_AMBIENTE + (A_LARG * CELL_SIZE) + GRID_SPACING    # A posição do tanque na tela depende da posição do ambiente
BASE_Y_TANQUE = -100

draw_grid(BASE_X_AMBIENTE, BASE_Y_AMBIENTE, A_ALT, A_LARG, "black")
draw_grid(BASE_X_TANQUE, BASE_Y_TANQUE, T_ALT, T_LARG, "black")

pen.penup()
pen.goto(BASE_X_AMBIENTE + (A_LARG*CELL_SIZE)/2, BASE_Y_AMBIENTE - 40)
pen.write("AMBIENTE", align="center", font=("Arial", 12, "bold"))
pen.goto(BASE_X_TANQUE + (T_LARG*CELL_SIZE)/2, BASE_Y_TANQUE - 40)
pen.write("TANQUE", align="center", font=("Arial", 12, "bold"))

# --- INICIALIZAÇÃO ---
posicao_carro = 0
atomos_tanque = {}
atomos_ambiente = {}
movs_restantes = n_movimentacoes

i = 1
for j in range(0, T_ALT):
    for k in range(0, T_LARG):
        atomos_tanque[i] = [k,j]
        i += 1


grid_tanque = np.zeros((T_ALT, T_LARG), dtype=int)
grid_ambiente = np.zeros((A_ALT, A_LARG), dtype=int)

for pos in atomos_tanque.values():
    x, y = pos
    grid_tanque[T_ALT - 1 - y, x] = 1
    
# Ambiente começa vazio

QUADRADO_TANQUE = [0, 0]
QUADRADO_AMBIENTE = [A_LARG - 1, 0]

print("Iniciando animação...")

# --- LOOP PRINCIPAL --- 
for frame in range(movs_restantes):
    
    # 1. Renderiza
    atom.clear()      # Primeiro limpa para garantir que nenhum átomo vai ficar por cima do outro
    hud.clear()       # Mesma coisa
    render_atoms(atomos_ambiente, BASE_X_AMBIENTE, BASE_Y_AMBIENTE, "royalblue")    # Atualiza a nova posição de cada átomo no tanque
    render_atoms(atomos_tanque, BASE_X_TANQUE, BASE_Y_TANQUE, "darkorange")         # Atualiza o ambiente
    
    
    hud.write(f"Movimento: {frame + 1}\nCarro na posição: {posicao_carro}",    # frame começa do 0, por isso somamos 1
              align="center", font=("Arial", 16, "bold"))
    
    wn.update()              # Como o tracer foi definido igual a 0 no início do código 
                             # temos que atualizar a janela pra aparecer tudo de uma vez
    time.sleep(VELOCIDADE)
    # 2. Mesma lógica do outro código
    todos_atomos_ids = list(atomos_tanque.keys()) + list(atomos_ambiente.keys())
    atom_id_selecionado = random.choice(todos_atomos_ids)

    pos_atual = None
    espaco_atual = None

    if atom_id_selecionado in atomos_tanque:
        pos_atual = atomos_tanque[atom_id_selecionado]
        espaco_atual = 'tanque'
    else:
        pos_atual = atomos_ambiente[atom_id_selecionado]
        espaco_atual = 'ambiente'

    direcao_nome = random.choice(list(direcoes.keys()))
    (dx, dy) = direcoes[direcao_nome]
    nova_pos = [pos_atual[0] + dx, pos_atual[1] + dy]

    if espaco_atual == 'tanque':
        if pos_atual == QUADRADO_TANQUE and direcao_nome == 'esquerda':
            target_x = QUADRADO_AMBIENTE[0]
            target_y = A_ALT - 1 - QUADRADO_AMBIENTE[1]
            if grid_ambiente[target_y, target_x] == 0:
                posicao_carro += 1
                atomos_tanque.pop(atom_id_selecionado)
                atomos_ambiente[atom_id_selecionado] = QUADRADO_AMBIENTE
                grid_tanque[T_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                grid_ambiente[target_y, target_x] = 1
        else:
            if (0 <= nova_pos[0] < T_LARG) and (0 <= nova_pos[1] < T_ALT):
                mat_y = T_ALT - 1 - nova_pos[1]
                mat_x = nova_pos[0]
                if grid_tanque[mat_y, mat_x] == 0:
                    grid_tanque[T_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                    grid_tanque[mat_y, mat_x] = 1
                    atomos_tanque[atom_id_selecionado] = nova_pos

    elif espaco_atual == 'ambiente':
        if pos_atual == QUADRADO_AMBIENTE and direcao_nome == 'direita':
            target_x = QUADRADO_TANQUE[0]
            target_y = T_ALT - 1 - QUADRADO_TANQUE[1]
            if grid_tanque[target_y, target_x] == 0:
                posicao_carro -= 1
                atomos_ambiente.pop(atom_id_selecionado)
                atomos_tanque[atom_id_selecionado] = QUADRADO_TANQUE
                grid_ambiente[A_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                grid_tanque[target_y, target_x] = 1
        else:
            if (0 <= nova_pos[0] < A_LARG) and (0 <= nova_pos[1] < A_ALT):
                mat_y = A_ALT - 1 - nova_pos[1]
                mat_x = nova_pos[0]
                if grid_ambiente[mat_y, mat_x] == 0:
                    grid_ambiente[A_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                    grid_ambiente[mat_y, mat_x] = 1
                    atomos_ambiente[atom_id_selecionado] = nova_pos

print("Fim da simulação.")
wn.mainloop()
