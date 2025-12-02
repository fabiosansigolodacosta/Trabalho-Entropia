import math
import random
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES ---
n_atomos = 9
n_simulacoes = 100  
n_movimentacoes = 10000  

tamanho_tanque = n_atomos
tamanho_ambiente = 25

direcoes = {'cima': (0, 1), 'baixo': (0, -1), 'direita': (1, 0), 'esquerda': (-1, 0)}

# Dimensões
T_LARG = int(math.sqrt(tamanho_tanque))
T_ALT = T_LARG
A_LARG = int(math.sqrt(tamanho_ambiente))
A_ALT = A_LARG

# Inicializa contagem
contagem_posicao = {}
for i in range(n_atomos + 1):
    contagem_posicao[i] = 0

print(f"Processando {n_simulacoes} simulações... Aguarde.")

# --- LOOP DAS SIMULAÇÕES ---
for simulacao in range(1, n_simulacoes + 1):
    posicao_carro = 0
    atomos_tanque = {}
    atomos_ambiente = {}
    movs_restantes = n_movimentacoes

    # 1. Preenche Dicionários (Início: Tudo no Tanque)(numero_atomo: pos(x, y))
    i = 1
    for j in range(0, T_ALT):       
        for k in range(0, T_LARG):   
            atomos_tanque[i] = [k,j] 
            i += 1

    # 2. Grids Lógicos
    grid_tanque = np.zeros((T_ALT, T_LARG), dtype=int)
    grid_ambiente = np.zeros((A_ALT, A_LARG), dtype=int)

    for pos in atomos_tanque.values():         # T_ALT - 1 pois começamos a contagem do zero;
        x, y = pos                             # -y pois nosso jeito de colocar as posições começa de baixo, a matriz por padrão tem a contagem começando por cima; 
        grid_tanque[T_ALT - 1 - y, x] = 1      # x e y foram invertidos pois, na matriz, o x representa a "altura", o y representa a coluna
        
    QUADRADO_TANQUE = [0, 0]                 # Quadrado especial que passa p/ o motor do carro
    QUADRADO_AMBIENTE = [A_LARG - 1, 0]      # 4, 0

    # --- MOVIMENTAÇÃO ---
    for _ in range(movs_restantes):
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
                target_x = QUADRADO_AMBIENTE[0] # 4              
                target_y = A_ALT - 1 - QUADRADO_AMBIENTE[1]  # 4    Posição do QUADRADO_AMBIENTE na matriz -> (4, 4)
                
                if grid_ambiente[target_y, target_x] == 0:      # Se estiver vazio anda, caso esteja cheio não faz nada
                    posicao_carro += 1
                    atomos_tanque.pop(atom_id_selecionado)
                    atomos_ambiente[atom_id_selecionado] = QUADRADO_AMBIENTE
                    grid_tanque[T_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                    grid_ambiente[target_y, target_x] = 1
            else:
                if (0 <= nova_pos[0] < T_LARG) and (0 <= nova_pos[1] < T_ALT):   
                    mat_y = T_ALT - 1 - nova_pos[1]   # mat_y e mat_x representam a nova pos. do átomo na matriz
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

    contagem_posicao[posicao_carro] += 1  #Dicionário que anota o num. de vezes que cada posição foi parada no fim de cada simulação

print(f'Contagem de posições: {contagem_posicao}')
# --- PREPARAÇÃO DOS DADOS ---
posicoes = list(contagem_posicao.keys())  #0 até 9 posições
contagem_final = list(contagem_posicao.values())
contagem_arr = np.array(contagem_final)

# Tratamento para Log: Substitui 0 por 1 (pois ln(1)=0)  np.where(cond., True, False)
contagem_segura = np.where(contagem_arr == 0, 1, contagem_arr) #Se o valor de simulações na posição for 0 vai ser colocado 0 no gráfico, pois ln(1) = 0
log_frequencia = np.log(contagem_segura)  # ln por padrão

# --- PLOTAGEM LADO A LADO ---
# Cria uma figura com 2 gráficos (1 linha, 2 colunas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# GRÁFICO 1: Frequência Absoluta (Azul)
ax1.bar(posicoes, contagem_final, color='cornflowerblue', edgecolor='black', alpha=0.9)
ax1.set_title(f"Frequência Absoluta (Linear)", fontsize=14)
ax1.set_xlabel("Posição do Carro", fontsize=12)
ax1.set_ylabel("Nº de Vezes", fontsize=12)
ax1.set_xticks(posicoes)
ax1.grid(linestyle='--', alpha=0.5)

# GRÁFICO 2: Entropia / Logaritmo (Laranja)
ax2.bar(posicoes, log_frequencia, color='orange', edgecolor='black', alpha=0.9)
ax2.set_title(f"Entropia: ln(Frequência)", fontsize=14)
ax2.set_xlabel("Posição do Carro", fontsize=12)
ax2.set_ylabel("ln(Ω)", fontsize=12)
ax2.set_xticks(posicoes)
ax2.set_ylim(bottom=0)
ax2.grid(linestyle='--', alpha=0.5)

plt.suptitle(f"Análise Estatística da Simulação ({n_simulacoes} Rodadas)", fontsize=16)
plt.show()

print(f'Na última simulação a disposição dos átomos no tanque ficou assim: (0 -> livre; 1 -> ocupado)\n{grid_tanque}')
print(f'Na última simulação a disposição dos átomos no ambiente ficou assim: (0 -> livre; 1 -> ocupado)\n{grid_ambiente}')
