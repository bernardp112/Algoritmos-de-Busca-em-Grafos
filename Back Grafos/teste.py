from bfs import bfs
from dfs import dfs_com_tempos

data = {
    "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
    "verticeInicial": "B",
    "matriz": [
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 1], # A
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0], # B
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], # C
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0], # D
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0], # E
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1], # F
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], # G
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0], # H
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], # I
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0], # J
        ]
    }

ordem, niveis = bfs(data)

print("Ordem de visita:", ordem)

print("\nNíveis dos vértices:")
for v in niveis:
    print(f"{v}: {niveis[v]}")


# Exemplo de uso
data = {
    "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
    "verticeInicial": "B",
    "matriz": [
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1],  # A
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],  # B
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # C
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # D
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],  # E
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # F
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],  # G
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],  # H
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # I
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # J
    ]
}

tempos, arvore, retorno = dfs_com_tempos(data)

print("\nTempos de descoberta/finalização:")
for v in tempos:
    print(f"{v}: {tempos[v]['descoberta']}, {tempos[v]['finalizacao']}")

print("\nArestas da árvore DFS:")
for pai, filho in arvore:
    print(f"{pai} -> {filho}")

print("\nArestas de retorno:")
for origem, destino in retorno:
    print(f"{origem} -> {destino}")