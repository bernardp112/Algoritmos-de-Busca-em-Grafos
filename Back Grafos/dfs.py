def dfs_com_tempos(data):
    vertices = data["vertices"]
    matriz = data["matriz"]
    vertice_inicial = data["verticeInicial"]

    visitados = set()
    tempo = 0
    tempos = {v: {"descoberta": None, "finalizacao": None} for v in vertices}
    arvore_dfs = []       # arestas de árvore (pai -> filho)
    arestas_retorno = []  # arestas de retorno (volta para ancestral)

    def dfs_recursivo(indice, pai=None):
        nonlocal tempo
        vertice = vertices[indice]
        visitados.add(vertice)
        tempo += 1
        tempos[vertice]["descoberta"] = tempo

        if pai:
            arvore_dfs.append((pai, vertice))

        # Explora vizinhos
        for i, conectado in enumerate(matriz[indice]):
            if conectado == 1:
                vizinho = vertices[i]
                # Se ainda não visitado → aresta de árvore
                if vizinho not in visitados:
                    dfs_recursivo(i, vertice)
                # Se visitado mas não finalizado → aresta de retorno
                elif tempos[vizinho]["finalizacao"] is None and vizinho != pai:
                    arestas_retorno.append((vertice, vizinho))

        tempo += 1
        tempos[vertice]["finalizacao"] = tempo

    # Executa o DFS a partir do vértice inicial
    dfs_recursivo(vertices.index(vertice_inicial))

    # Executa DFS para componentes desconectados
    for i, v in enumerate(vertices):
        if v not in visitados:
            dfs_recursivo(i)

    return tempos, arvore_dfs, arestas_retorno