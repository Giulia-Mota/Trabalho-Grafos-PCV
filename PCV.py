# Feito por Giulia Mota Apinagés dos Santos e José Vitor Alves

import random

# Matriz de distâncias lau15
distancias = [
    [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
    [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
    [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
    [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
    [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
    [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
    [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51, 46, 33],
    [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33, 31, 37],
    [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29, 51, 11],
    [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 21, 41, 23, 37],
    [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42, 59, 61],
    [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61, 11, 55],
    [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0, 62, 23],
    [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0, 59],
    [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0]
]

# Parâmetros do algoritmo
num_formigas = 20          # Número de formigas
iteracoes = 100            # Número de iterações
alfa = 1.0                 # Peso dos feromônios
beta = 2.0                 # Peso da heurística (1/distância)
taxa_evaporacao = 0.5      # Taxa de evaporação dos feromônios
Q = 100                    # Constante para atualização de feromônios

# Número de cidades
n = len(distancias)

# Inicialização da matriz de feromônios
feromonios = [[1.0 for _ in range(n)] for _ in range(n)]

# Função para calcular a probabilidade de escolher a próxima cidade
def escolha_prox_cidade(atual, visitada, feromonios, distancias, alfa, beta):
    probabilidades = []
    total = 0.0

    for cidade in range(n):
        if cidade not in visitada:
            feromonio = feromonios[atual][cidade] ** alfa
            heuristica = (1.0 / distancias[atual][cidade]) ** beta
            probabilidades.append((cidade, feromonio * heuristica))
            total += feromonio * heuristica

    # Normaliza as probabilidades
    probabilidades = [(cidade, prob / total) for cidade, prob in probabilidades]

    # Escolhe a próxima cidade com base nas probabilidades
    r = random.random()
    prob_cumulativa = 0.0
    for cidade, prob in probabilidades:
        prob_cumulativa += prob
        if r <= prob_cumulativa:
            return cidade
    return probabilidades[-1][0]

# Função para calcular o custo de um caminho
def calc_custo(caminho, distancias):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += distancias[caminho[i]][caminho[i + 1]]
    custo += distancias[caminho[-1]][caminho[0]]  # Retorna ao início
    return custo

# Função para atualizar os feromônios
def atualiza_feromonio(feromonios, caminhos, taxa_evaporacao, q):
    # Evaporação dos feromônios
    for i in range(n):
        for j in range(n):
            feromonios[i][j] *= (1.0 - taxa_evaporacao)

    # Adiciona novos feromônios com base nos caminhos das formigas
    for caminho, custo in caminhos:
        for i in range(len(caminho) - 1):
            feromonios[caminho[i]][caminho[i + 1]] += q / custo
        feromonios[caminho[-1]][caminho[0]] += q / custo  # Feromônio no ciclo de retorno

# Algoritmo de Colônia de Formigas
def pcv_aco(distancias, num_formigas, iteracoes, alfa, beta, taxa_evaporacao, q):
    melhorCaminho = None
    melhorCusto = float('inf')

    for iteracao in range(iteracoes):
        caminhos = []
        for formiga in range(num_formigas):
            caminho = [0]  # Começa na cidade 0
            visitada = {0}

            while len(caminho) < n:
                atual = caminho[-1]
                proxCidade = escolha_prox_cidade(atual, visitada, feromonios, distancias, alfa, beta)
                caminho.append(proxCidade)
                visitada.add(proxCidade)

            caminho.append(0)  # Retorna à cidade inicial
            custo = calc_custo(caminho, distancias)
            caminhos.append((caminho, custo))

            if custo < melhorCusto:
                melhorCusto = custo
                melhorCaminho = caminho

        atualiza_feromonio(feromonios, caminhos, taxa_evaporacao, Q)

        print(f"Iteração {iteracao + 1}: Melhor custo = {melhorCusto}")

    return melhorCaminho, melhorCusto

# Executa o algoritmo
melhorCaminho, melhorCusto = pcv_aco(distancias, num_formigas, iteracoes, alfa, beta, taxa_evaporacao, Q)

# Exibe o resultado
print(f"\nMelhor caminho encontrado: {melhorCaminho}")
print(f"Custo do melhor caminho: {melhorCusto}")