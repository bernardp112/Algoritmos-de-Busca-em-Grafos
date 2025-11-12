"""
Módulo para gerar visualizações ASCII dos algoritmos BFS e DFS
"""

def gerar_ascii_bfs(ordem, niveis, arvore=None):
    """
    Gera uma representação ASCII da execução do BFS
    
    Args:
        ordem: Lista de componentes (lista de listas) com a ordem de visita
        niveis: Dicionário {vértice: nível}
        arvore: Lista opcional de tuplas (pai, filho) representando a árvore BFS
    
    Returns:
        String com a visualização ASCII
    """
    # TODO: Implementar visualização ASCII do BFS
    # Aguardando especificação do formato desejado
    
    lines = []
    lines.append("=" * 60)
    lines.append("BFS - Execução passo a passo")
    lines.append("=" * 60)
    lines.append("")
    
    # Normalizar ordem: garantir que seja lista de listas
    if ordem and isinstance(ordem[0], str):
        ordem = [ordem]

    # Para cada componente conexo
    for comp_idx, componente in enumerate(ordem):
        if comp_idx > 0:
            lines.append("")

        # Exibir ordem de execução no formato [A0, B1, S1, ...]
        vertices_formatados = []
        for v in componente:
            nivel = niveis.get(v)
            if nivel is not None:
                vertices_formatados.append(f"{v}{nivel}")
            else:
                vertices_formatados.append(f"{v}")
        lines.append(f"[{', '.join(vertices_formatados)}]")

    return "\n".join(lines)


def gerar_ascii_dfs(tempos, arvore, arestas_retorno, is_directed=False, matriz=None, vertices=None):
    """
    Gera uma representação ASCII da execução do DFS
    
    Args:
        tempos: Dicionário {vértice: {"descoberta": int, "finalizacao": int}}
        arvore: Lista de tuplas (pai, filho) representando a árvore DFS
        arestas_retorno: Lista de tuplas (origem, destino) das back edges
        is_directed: Boolean indicando se o grafo é direcionado (para usar setinhas)
        matriz: Matriz de adjacência (para verificar bidirecionality)
        vertices: Lista de vértices (para mapear índices da matriz)
    
    Returns:
        String com a visualização ASCII
    """
    lines = []
    lines.append("=" * 60)
    lines.append("DFS - Execução passo a passo")
    lines.append("=" * 60)
    lines.append("")
    
    # Função helper para verificar se existe aresta bidirecional
    def is_bidirectional(u, v):
        """Verifica se existe aresta u→v E v→u na matriz"""
        if not matriz or not vertices:
            return False
        try:
            idx_u = vertices.index(u)
            idx_v = vertices.index(v)
            # Existe u→v E v→u?
            return matriz[idx_u][idx_v] != 0 and matriz[idx_v][idx_u] != 0
        except (ValueError, IndexError):
            return False
    
    # Se a árvore vier vazia ou incompleta, inferir estrutura pelos tempos
    # Um vértice V é filho de U se foi descoberto durante a execução de U
    # (descoberta[V] > descoberta[U] e finalizacao[V] < finalizacao[U])
    
    if not arvore:
        # Construir árvore a partir dos tempos de descoberta/finalização
        arvore = []
        vertices_ordenados = sorted(tempos.keys(), key=lambda x: tempos[x]["descoberta"])
        
        for v in vertices_ordenados:
            d_v = tempos[v]["descoberta"]
            f_v = tempos[v]["finalizacao"]
            
            # Encontrar o pai mais próximo (último vértice que contém v)
            pai_candidato = None
            melhor_distancia = float('inf')
            
            for u in vertices_ordenados:
                if u == v:
                    continue
                d_u = tempos[u]["descoberta"]
                f_u = tempos[u]["finalizacao"]
                
                # u contém v se d_u < d_v < f_v < f_u
                if d_u < d_v < f_v < f_u:
                    distancia = d_v - d_u
                    if distancia < melhor_distancia:
                        melhor_distancia = distancia
                        pai_candidato = u
            
            if pai_candidato:
                arvore.append((pai_candidato, v))
    
    # Construir estrutura de árvore
    children = {}
    parent = {}
    all_in_tree = set()
    
    for pai, filho in arvore:
        if pai not in children:
            children[pai] = []
        children[pai].append(filho)
        parent[filho] = pai 
        all_in_tree.add(pai)
        all_in_tree.add(filho)
    
    # Todos os vértices que têm tempo (foram visitados)
    all_vertices_visited = set(tempos.keys())
    
    # Encontrar raízes (vértices que aparecem na árvore mas não são filhos de ninguém)
    roots = [v for v in all_in_tree if v not in parent]
    
    # Se ainda não há raízes, pegar os primeiros descobertos
    if not roots:
        roots = [min(tempos.keys(), key=lambda x: tempos[x]["descoberta"])]
    
    # Criar dict de arestas de retorno por origem
    retornos_por_origem = {}
    for origem, destino in arestas_retorno:
        if origem not in retornos_por_origem:
            retornos_por_origem[origem] = []
        retornos_por_origem[origem].append(destino)
    
    # Função recursiva para desenhar a árvore
    def draw_tree(node, prefix="", is_last=True, parent_node=None):
        # Descoberta e finalização
        d = tempos[node]["descoberta"]
        f = tempos[node]["finalizacao"]
        
        # Verificar se a aresta parent→node é bidirecional no grafo original
        is_bidir = parent_node and is_bidirectional(parent_node, node)
        
        # Símbolo do conector
        if is_directed and not is_bidir:
            # Direcionado e NÃO bidirecional: usar seta
            connector = "└──> " if is_last else "├──> "
        else:
            # Não direcionado OU bidirecional: sem seta
            connector = "└── " if is_last else "├── "
        
        # Primeira linha ou continuação
        if prefix == "":
            lines.append(f"{node}({d}/{f})")
        else:
            lines.append(f"{prefix}{connector}{node}({d}/{f})")
        
        # Se este nó tem arestas de retorno, mostrar logo abaixo
        if node in retornos_por_origem:
            extension = "    " if is_last else "│   "
            retorno_prefix = prefix + extension if prefix else extension
            for destino in retornos_por_origem[node]:
                lines.append(f"{retorno_prefix}    ↖ Retorno para {destino}")
        
        # Recursão para os filhos
        node_children = children.get(node, [])
        # Ordenar filhos por tempo de descoberta
        node_children.sort(key=lambda x: tempos[x]["descoberta"])
        
        for i, child in enumerate(node_children):
            is_last_child = (i == len(node_children) - 1)
            extension = "    " if is_last else "│   "
            # Para a raiz (prefix vazio), começar com extension; senão, concatenar
            new_prefix = prefix + extension if prefix else extension
            draw_tree(child, new_prefix, is_last_child, parent_node=node)
    
    # Desenhar cada componente (pode haver múltiplas raízes)
    if roots:
        roots_sorted = sorted(roots, key=lambda x: tempos[x]["descoberta"])
        
        for i, root in enumerate(roots_sorted):
            if i > 0:
                lines.append("")
            draw_tree(root)
        
        # Se algum vértice visitado não apareceu na árvore, listar separadamente
        vertices_in_tree = set()
        for r in roots_sorted:
            def collect_vertices(node):
                vertices_in_tree.add(node)
                for child in children.get(node, []):
                    collect_vertices(child)
            collect_vertices(r)
        
        orphans = all_vertices_visited - vertices_in_tree
        if orphans:
            for orphan in sorted(orphans, key=lambda x: tempos[x]["descoberta"]):
                lines.append("")
                d = tempos[orphan]["descoberta"]
                f = tempos[orphan]["finalizacao"]
                lines.append(f"{orphan}({d}/{f})")
    else:
        # Fallback: se não há raízes, listar todos
        for v in sorted(all_vertices_visited, key=lambda x: tempos[x]["descoberta"]):
            d = tempos[v]["descoberta"]
            f = tempos[v]["finalizacao"]
            lines.append(f"{v}({d}/{f})")
    
    return "\n".join(lines)
