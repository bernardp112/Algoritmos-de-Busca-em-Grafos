from collections import deque

def bfs(data):
    vertices = data["vertices"]
    matriz = data["matriz"]
    vertice_inicial = data["verticeInicial"]

    visitados = set()
    componentes = []       # lista de listas (cada componente = uma BFS)
    arvore_bfs = []        # pares (pai, filho)
    niveis = {v: None for v in vertices}  # distância (nível)

    def bfs_componente(inicio):
        fila = deque([inicio])
        visitados.add(inicio)
        niveis[inicio] = 0
        ordem_local = []

        while fila:
            atual = fila.popleft()
            ordem_local.append(atual)
            indice_atual = vertices.index(atual)

            for i, conectado in enumerate(matriz[indice_atual]):
                vizinho = vertices[i]
                if conectado == 1 and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
                    arvore_bfs.append((atual, vizinho))
                    niveis[vizinho] = niveis[atual] + 1

        return ordem_local

    # 1️⃣ Começa com o vértice inicial
    componentes.append(bfs_componente(vertice_inicial))

    # 2️⃣ Explora componentes desconectados
    for v in vertices:
        if v not in visitados:
            componentes.append(bfs_componente(v))

    return componentes, niveis