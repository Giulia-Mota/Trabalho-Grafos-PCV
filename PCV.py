#Feito por Giulia Mota Apinagés dos Santos e José Vitor Alves

import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def ler_matriz(arquivo):
    with open(arquivo, "r") as f:
        linhas = f.readlines()
    matriz = [list(map(int, linha.split())) for linha in linhas if linha.strip()]
    return np.array(matriz)


def calcular_custo(matriz, caminho):
    custo = sum(matriz[caminho[i]][caminho[i + 1]] for i in range(len(caminho) - 1))
    custo += matriz[caminho[-1]][caminho[0]]
    return custo


def ant_system(matriz, formigas, iteracoes, alfa=1, beta=5, rho=0.5, Q=100):
    cidades = len(matriz)
    feromonio = np.full((cidades, cidades), 1e-6)
    melhor_caminho = []
    melhor_custo = float('inf')

    for _ in range(iteracoes):
        caminhos = []
        custos = []

        for _ in range(formigas):
            caminho = []
            visitadas = [False] * cidades
            cidade_atual = random.randint(0, cidades - 1)
            caminho.append(cidade_atual)
            visitadas[cidade_atual] = True

            while len(caminho) < cidades:
                probabilidades = []
                for j in range(cidades):
                    if not visitadas[j]:
                        eta = 1 / matriz[cidade_atual][j]
                        tau_ij = feromonio[cidade_atual][j]
                        probabilidade = (tau_ij ** alfa) * (eta ** beta)
                        probabilidades.append(probabilidade)
                    else:
                        probabilidades.append(0)

                total_probabilidade = sum(probabilidades)
                probabilidades = [p / total_probabilidade for p in probabilidades]
                prox_cidade = random.choices(range(cidades), weights=probabilidades)[0]
                caminho.append(prox_cidade)
                visitadas[prox_cidade] = True
                cidade_atual = prox_cidade

            caminhos.append(caminho)
            custo = calcular_custo(matriz, caminho)
            custos.append(custo)

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_caminho = caminho

        feromonio *= (1 - rho)
        for k in range(formigas):
            caminho = caminhos[k]
            custo = custos[k]
            for i in range(cidades - 1):
                feromonio[caminho[i]][caminho[i + 1]] += Q / custo
            feromonio[caminho[-1]][caminho[0]] += Q / custo

    return melhor_caminho, melhor_custo


def visualizar_caminho(grafo, caminho):
    grafo_caminho = nx.DiGraph()
    for i in range(len(caminho) - 1):
        grafo_caminho.add_edge(caminho[i], caminho[i + 1], weight=grafo[caminho[i]][caminho[i + 1]]['weight'])
    grafo_caminho.add_edge(caminho[-1], caminho[0], weight=grafo[caminho[-1]][caminho[0]]['weight'])

    pos = nx.spring_layout(grafo_caminho)
    nx.draw(grafo_caminho, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='black', arrows=True)
    plt.show()


def main():
    arquivo = "lau15_dist.txt"
    matriz = ler_matriz(arquivo)

    formigas = len(matriz)
    iteracoes = 100
    melhor_caminho, melhor_custo = ant_system(matriz, formigas, iteracoes)

    print("Melhor caminho encontrado:", melhor_caminho)
    print("Custo total do melhor caminho:", melhor_custo)

    grafo = nx.DiGraph()
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if i != j:
                grafo.add_edge(i, j, weight=matriz[i][j])

    visualizar_caminho(grafo, melhor_caminho)


if __name__ == "__main__":
    main()