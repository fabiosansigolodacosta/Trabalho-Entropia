import math
import random
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES ---
n_atomos = 9 
atomos_tanque = n_atomos 
atomos_ambiente = 0 
tamanho_tanque = atomos_tanque
tamanho_ambiente = 25 

# AUMENTADO: Para garantir estatística relevante
n_simulacoes = 500
n_movimentacoes = 10000 

contagem_posicao = {}
for i in range(n_atomos + 1):
    contagem_posicao[i] = 0

direcoes = {'cima': (0, 1), 'baixo': (0, -1), 'direita': (1, 0), 'esquerda': (-1, 0)}

# Dimensões (Eu limpei os espaços invisíveis aqui!)
T_LARG = int(math.sqrt(tamanho_tanque)) 
T_ALT = T_LARG  
A_LARG = int(math.sqrt(tamanho_ambiente)) 
A_ALT = A_LARG  

print(f"Rodando {n_simulacoes} simulações para gerar a curva estatística...")

# --- SIMULAÇÃO ---
for simulacao in range(1, n_simulacoes + 1):
    posicao_carro = 0 
    atomos_tanque = {}
    atomos_ambiente = {}
    movs_restantes = n_movimentacoes

    # 1. PREENCHE DICIONÁRIOS
    i = 1
    for j in range(0, T_ALT):       
        for k in range(0, T_LARG):   
            atomos_tanque[i] = [k,j]
            i += 1

    # 2. CONDIÇÃO INICIAL (Baseada na imagem)
    if len(atomos_tanque) == n_atomos:
        atomos_tanque.pop(1) 
        atomos_ambiente[1] = [A_LARG - 1, 0] 
        movs_restantes -= 1
        posicao_carro += 1

    # 3. CRIAÇÃO DOS GRIDS (Visual)
    grid_tanque = np.zeros((T_ALT, T_LARG), dtype=int)
    grid_ambiente = np.zeros((A_ALT, A_LARG), dtype=int)

    # Arrumamos aqui: Usamos a matemática direta para inverter, sem usar transpose
    for pos in atomos_tanque.values():
        x, y = pos
        # Inverte Y para ficar igual ao plano cartesiano (0 embaixo)
        grid_tanque[T_ALT - 1 - y, x] = 1 
        
    for pos in atomos_ambiente.values():
        x, y = pos
        grid_ambiente[A_ALT - 1 - y, x] = 1

    QUADRADO_TANQUE = [0, 0]    
    QUADRADO_AMBIENTE = [A_LARG - 1, 0] 

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

        # LÓGICA DE MOVIMENTO
        if espaco_atual == 'tanque':
            if pos_atual == QUADRADO_TANQUE and direcao_nome == 'esquerda':
                # Limpei a confusão que estava aqui
                target_x = QUADRADO_AMBIENTE[0] # Porta
                target_y = A_ALT - 1 - QUADRADO_AMBIENTE[1] # Andar (Invertido)
                
                if grid_ambiente[target_y, target_x] == 0: 
                    posicao_carro += 1
                    atomos_tanque.pop(atom_id_selecionado)
                    atomos_ambiente[atom_id_selecionado] = QUADRADO_AMBIENTE
                    
                    grid_tanque[T_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                    grid_ambiente[target_y, target_x] = 1
            else:
                if (0 <= nova_pos[0] < T_LARG) and (0 <= nova_pos[1] < T_ALT):
                    # Andar (Invertido)
                    mtx_y = T_ALT - 1 - nova_pos[1]
                    # Porta
                    mtx_x = nova_pos[0]
                    
                    if grid_tanque[mtx_y, mtx_x] == 0:
                        grid_tanque[T_ALT - 1 - pos_atual[1], pos_atual[0]] = 0 
                        grid_tanque[mtx_y, mtx_x] = 1   
                        atomos_tanque[atom_id_selecionado] = nova_pos

        elif espaco_atual == 'ambiente':
            if pos_atual == QUADRADO_AMBIENTE and direcao_nome == 'direita':
                target_x = QUADRADO_TANQUE[0] # Porta
                target_y = T_ALT - 1 - QUADRADO_TANQUE[1] # Andar (Invertido)
                
                if grid_tanque[target_y, target_x] == 0: 
                    posicao_carro -= 1
                    atomos_ambiente.pop(atom_id_selecionado)
                    atomos_tanque[atom_id_selecionado] = QUADRADO_TANQUE
                    
                    grid_ambiente[A_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                    grid_tanque[target_y, target_x] = 1
            else:
                if (0 <= nova_pos[0] < A_LARG) and (0 <= nova_pos[1] < A_ALT):
                    mtx_y = A_ALT - 1 - nova_pos[1]
                    mtx_x = nova_pos[0]
                    
                    if grid_ambiente[mtx_y, mtx_x] == 0:
                        grid_ambiente[A_ALT - 1 - pos_atual[1], pos_atual[0]] = 0
                        grid_ambiente[mtx_y, mtx_x] = 1
                        atomos_ambiente[atom_id_selecionado] = nova_pos

    contagem_posicao[posicao_carro] += 1

# --- PLOTAGEM ---
posicoes = list(contagem_posicao.keys()) 
contagem_final = list(contagem_posicao.values())

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(posicoes, contagem_final, color='royalblue', edgecolor='black', alpha=0.8)

ax.set_title(f"Distribuição de Frequência ({n_simulacoes} Simulações)", fontsize=14)
ax.set_xlabel("Posição do Carro (Nº Átomos no Ambiente)", fontsize=12)
ax.set_ylabel("Número de Simulações (Vezes)", fontsize=12)

ax.grid(linestyle='--', alpha=0.5)
ax.set_xticks(posicoes) 
ax.set_ylim(bottom=0)

plt.show()

print("--- Grid Tanque Final (Visual) ---")
print(grid_tanque)
print("\n--- Grid Ambiente Final (Visual) ---")
print(grid_ambiente)
print(f"Posição Final do Carro: {posicao_carro}")
