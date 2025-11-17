import math
import random

#ÁTOMOS NO TANQUE
#[0,2][1,2][2,2]
#[0,1][1,1][2,1]
#[0,0][1,0][2,0]

#ÁTOMOS NO AMBIENTE
#[0,4][1,4][2,4][3,4][4,4]
#[0,3][1,3][2,3][3,3][4,3]
#[0,2][1,2][2,2][3,2][4,2]
#[0,1][1,1][2,1][3,1][4,1]
#[0,0][1,0][2,0][3,0][4,0]

#Parte 1 -> VARIÁVEIS
n_atomos = 9 # Tem que ser um quadrado perfeito. No exemplo é 9
atomos_tanque = n_atomos 
atomos_ambiente = 0
tamanho_tanque = atomos_tanque
tamanho_ambiente = 25 # Também tem que ser quadrado perfeito. No exemplo é 25
n_movimentacoes = 100000 # Número arbitrário que representa as tentativas de variações na pos. do átomo
direcoes = {'cima': (0, 1), 'baixo': (0, -1), 'direita': (1, 0), 'esquerda': (-1, 0)} # Define as variações sobre cada movimento do átomo
posicao_carro = 0 # Carro começa na posição 0

T_LARG = int(math.sqrt(tamanho_tanque)) # Largura do Tanque -> no exemplo é igual a 3
T_ALT = int(math.sqrt(tamanho_tanque))  # Altura do Tanque -> no exemplo é igual a 3
A_LARG = int(math.sqrt(tamanho_ambiente)) # Largura do Ambiente -> no exemplo é igual a 5
A_ALT = int(math.sqrt(tamanho_ambiente))  # Altura do Ambiente -> no exemplo é igual a 5


#Parte 2 -> MOVIMENTAÇÃO ALEATÓRIA DOS ÁTOMOS

atomos_tanque = {}
atomos_ambiente = {}


i = 1
for j in range(0, int(math.sqrt(n_atomos))):       # Cria um dicionário com as posições iniciais de cada átomo no formato (x, y)  
    for k in range(0, int(math.sqrt(n_atomos))):   #Ex: {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
        atomos_tanque[i] = [k,j]
        i += 1

#2.2 -> SITUAÇÃO INICIAL(OCORRE INDEPENDENTE DE TUDO)
if len(atomos_tanque) == n_atomos:
    atomos_tanque.pop(1)
    atomos_ambiente[1] = [int(math.sqrt(tamanho_ambiente) - 1),0]
    n_movimentacoes -= 1
    posicao_carro += 1

# Defina quais são os quadrados de entrada/saída
QUADRADO_TANQUE = [0, 0]     # Posição no tanque que leva ao motor
QUADRADO_AMBIENTE = [int(math.sqrt(tamanho_ambiente) - 1), 0] # Posição no ambiente que vem do motor

# Roda a simulação pelo número de movimentos restantes
for _ in range(n_movimentacoes):
    
    # 1. Escolhe um átomo aleatório (de QUALQUER lugar)
    # Pega todos os IDs de átomos que existem
    todos_atomos_ids = list(atomos_tanque.keys()) + list(atomos_ambiente.keys()) # 1, 2, 3, ..., n_atomos
    atom_id_selecionado = random.choice(todos_atomos_ids) 

    # 2. Descobre onde ele está (tanque ou ambiente)
    pos_atual = None
    espaco_atual = None

    if atom_id_selecionado in atomos_tanque:
        pos_atual = atomos_tanque[atom_id_selecionado]
        espaco_atual = 'tanque'
    else: #No caso do átomo estar no ambiente
        pos_atual = atomos_ambiente[atom_id_selecionado]
        espaco_atual = 'ambiente'

    # 3. Escolhe uma direção aleatória
    # direcoes = {'cima': (0, 1), 'baixo': (0, -1), 'direita': (1, 0), 'esquerda': (-1, 0)}
    direcao_nome = random.choice(list(direcoes.keys())) #cima, baixo, direita ou esquerda
    (dx, dy) = direcoes[direcao_nome]
    
    # 4. Calcula a nova posição
    nova_pos = [pos_atual[0] + dx, pos_atual[1] + dy]

    # 5. APLICA A LÓGICA DE MOVIMENTO E COLISÃO
    
    if espaco_atual == 'tanque':
        # 5a. VERIFICA SE O ÁTOMO BATEU NO QUADRADO DO AMBIENTE PARA SAIR
        # (Ex: se está no [0,0] e move para 'esquerda')
        if pos_atual == QUADRADO_TANQUE and direcao_nome == 'esquerda':
            if QUADRADO_AMBIENTE not in atomos_ambiente.values():   #Verifica se o quadrado de entrada no ambiente tá livre
                posicao_carro += 1
            # Move o átomo do tanque para o ambiente e o carro anda 1 posição p/ frente
                atomos_tanque.pop(atom_id_selecionado) # Tira o átomo do tanque
                atomos_ambiente[atom_id_selecionado] = QUADRADO_AMBIENTE # E coloca no quadrado de entrada do outro lado

                
        
        # 5b. Se não bateu no quadrado, tenta mover DENTRO do tanque
        else:
            # Verifica se a nova_pos está dentro dos limites do tanque (0 a 2)
            if (0 <= nova_pos[0] < T_LARG) and (0 <= nova_pos[1] < T_ALT):
                # Verifica se a nova_pos NÃO está ocupada por outro átomo 
                if nova_pos not in atomos_tanque.values():
                    # Move o átomo
                    atomos_tanque[atom_id_selecionado] = nova_pos

                    
            # Se bateu na parede ou em outro átomo, não faz nada

    
    elif espaco_atual == 'ambiente':
        # 5c. VERIFICA SE O ÁTOMO BATEU NO QUADRADO PARA VOLTAR
        # (Ex: se está no [4,0] e move para 'direita'
        if pos_atual == QUADRADO_AMBIENTE and direcao_nome == 'direita':
            if QUADRADO_TANQUE not in atomos_tanque.values(): # Verifica se o quadrado de entrada no tanque não está ocupado
                posicao_carro -= 1 # O carro volta uma casa
                # Move o átomo do ambiente para o tanque
                atomos_ambiente.pop(atom_id_selecionado)
                atomos_tanque[atom_id_selecionado] = QUADRADO_TANQUE # Coloca no quadrado de entrada do outro lado

                

        # 5d. Se não, tenta mover DENTRO do ambiente
        else:
            # Verifica se a nova_pos está dentro dos limites do ambiente (0 a 4)
            if (0 <= nova_pos[0] < A_LARG) and (0 <= nova_pos[1] < A_ALT):
                # Verifica se a nova_pos NÃO está ocupada
                if nova_pos not in atomos_ambiente.values():
                    # Move o átomo
                    atomos_ambiente[atom_id_selecionado] = nova_pos

                   
            # Se bateu na parede ou em outro átomo, não faz nada

# --- Fim ---
print(f"Episódio terminou. Posição final do carro: {posicao_carro}")
print(f"Átomos no tanque: {len(atomos_tanque)}, Átomos no ambiente: {len(atomos_ambiente)}")
print(f"Organização dos átomos no tanque: {atomos_tanque}")
print(f"Organização dos átomos no ambiente: {atomos_ambiente}")