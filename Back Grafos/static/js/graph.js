// ============================================
// GRAPH.JS - Funções de Renderização do Grafo
// ============================================

(function() {
  const getElement = (selector) => document.querySelector(selector);
  const App = window.App = window.App || {};

  // ============================================
  // LEITURA DO JSON
  // ============================================
  
  /**
   * Lê e valida o JSON do textarea
   * @returns {Object} Dados do grafo parseados
   * @throws {Error} Se o JSON for inválido
   */
  App.readPayload = function readPayload() {
    const jsonText = getElement("#payload").value;
    
    try {
      return JSON.parse(jsonText);
    } catch (error) {
      getElement("#output").textContent = "JSON inválido: " + error.message;
      throw error;
    }
  };
  
  // VERIFICAÇÃO DE SIMETRIA DA MATRIZ
  
  /**
   * Verifica se a matriz de adjacência é simétrica (grafo não-direcionado)
   * @param {Array} matrix - Matriz de adjacência
   * @returns {boolean} true se for simétrica (não-direcionado)
   */
  App.isSymmetric = function isSymmetric(matrix) {
    // Verificar se é uma matriz válida
    if (!Array.isArray(matrix)) return false;
    
    const size = matrix.length;
    
    for (let i = 0; i < size; i++) {
      // Verificar se cada linha é um array do tamanho correto
      if (!Array.isArray(matrix[i]) || matrix[i].length !== size) {
        return false;
      }
      
      // Comparar apenas metade superior da matriz (otimização)
      for (let j = i + 1; j < size; j++) {
        const valueIJ = matrix[i][j] || 0;
        const valueJI = matrix[j][i] || 0;
        
        // Se M[i][j] != M[j][i], não é simétrica
        if (valueIJ !== valueJI) {
          return false;
        }
      }
    }
    
    return true;
  };

  // ============================================
  // CONSTRUÇÃO DE NÓS E ARESTAS
  // ============================================
  
  /**
   * Constrói os elementos (nós e arestas) do grafo para o Cytoscape
   * @param {Object} payload - Dados do grafo {vertices, matriz}
   * @returns {Object} {nodes, edges, undirected}
   */
  App.buildElements = function buildElements(payload) {
    const vertices = payload.vertices || [];
    const matrix = payload.matriz || [];
    
    // Criar nós (vértices)
    const nodes = vertices.map(vertex => ({
      data: { id: vertex, label: vertex }
    }));
    
    const edges = [];
    
    // Verificar se o grafo é direcionado ou não
    const isUndirected = App.isSymmetric(matrix);
    
    if (isUndirected) {
      // GRAFO NÃO-DIRECIONADO: Processar apenas metade da matriz
      for (let i = 0; i < matrix.length; i++) {
        for (let j = i + 1; j < (matrix[i] || []).length; j++) {
          const hasEdge = (matrix[i][j] || 0) === 1 || (matrix[j][i] || 0) === 1;
          
          if (hasEdge) {
            const vertexA = vertices[i];
            const vertexB = vertices[j];
            
            edges.push({
              data: {
                id: `${vertexA}--${vertexB}`,
                source: vertexA,
                target: vertexB
              },
              classes: 'undirected' // Marca como não-direcionado (sem seta)
            });
          }
        }
      }
    } else {
      // GRAFO DIRECIONADO: Processar toda a matriz
      for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < (matrix[i] || []).length; j++) {
          if (matrix[i][j] === 1) {
            const source = vertices[i];
            const target = vertices[j];
            
            edges.push({
              data: {
                id: `${source}-${target}`,
                source: source,
                target: target
              }
            });
          }
        }
      }
    }
    
    return { nodes, edges, undirected: isUndirected };
  };

  // INICIALIZAÇÃO DO CYTOSCAPE
  
  /**
   * Inicializa o Cytoscape com os elementos e layout
   * @param {Object} elements - {nodes, edges} do grafo
   * @param {string} layoutName - Nome do layout ('cose', 'circle', etc.)
   */
  App.initCy = function initCy(elements, layoutName = 'cose') {
    // Destruir instância anterior se existir
    if (App.cy) {
      App.cy.destroy();
    }
    
    // Criar nova instância do Cytoscape
    App.cy = cytoscape({
      container: document.getElementById('cy'),
      elements: [ ...elements.nodes, ...elements.edges ],
      
      // Estilos visuais
      style: [
        { selector: 'node', style: {
          'label': 'data(label)',
          'background-color': '#4f46e5',
          'color': '#111',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': '12px',
          'width': '28px',
          'height': '28px',
          'border-width': 1,
          'border-color': '#1114'
        }},
        { selector: 'node.lane', style: {
          'shape': 'round-rectangle',
          'background-color': '#94a3b8',
          'opacity': 0.25,
          'width': 'data(w)',
          'height': 'data(h)',
          'border-width': 0,
          'label': 'data(label)',
          'text-halign': 'left',
          'text-valign': 'top',
          'text-margin-x': 8,
          'text-margin-y': 6,
          'z-index': 0
        }},
        { selector: 'edge', style: {
          'line-color': '#64748b',
          'width': 2,
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#64748b',
          'curve-style': 'bezier'
        }},
        { selector: 'edge.undirected', style: {
          'target-arrow-shape': 'none',
          'source-arrow-shape': 'none'
        }},
        { selector: 'edge.tree-edge', style: {
          'line-color': '#16a34a',
          'target-arrow-color': '#16a34a',
          'width': 3
        }},
        { selector: 'edge.back-edge', style: {
          'line-color': '#dc2626',
          'target-arrow-color': '#dc2626',
          'line-style': 'dashed'
        }},
        { selector: 'edge.faded', style: {
          'opacity': 0.2
        }}
      ],
      layout: { name: layoutName, animate: true }
    });
  };

  App.initCyWithPositions = function initCyWithPositions(elements, positions){
    if (App.cy) App.cy.destroy();
    App.cy = cytoscape({
      container: document.getElementById('cy'),
      elements: [ ...elements.nodes, ...elements.edges ],
      style: [
        { selector: 'node', style: {
          'label': 'data(label)',
          'background-color': '#4f46e5',
          'color': '#111',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': '12px',
          'width': '28px',
          'height': '28px',
          'border-width': 1,
          'border-color': '#1114'
        }},
        { selector: 'node.lane', style: {
          'shape': 'round-rectangle',
          'background-color': '#94a3b8',
          'opacity': 0.25,
          'width': 'data(w)',
          'height': 'data(h)',
          'border-width': 0,
          'label': 'data(label)',
          'text-halign': 'left',
          'text-valign': 'top',
          'text-margin-x': 8,
          'text-margin-y': 6,
          'z-index': 0
        }},
        { selector: 'edge', style: {
          'line-color': '#64748b',
          'width': 2,
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#64748b',
          'curve-style': 'bezier'
        }},
        { selector: 'edge.undirected', style: {
          'target-arrow-shape': 'none',
          'source-arrow-shape': 'none'
        }},
        { selector: 'edge.tree-edge', style: {
          'line-color': '#16a34a',
          'target-arrow-color': '#16a34a',
          'width': 3
        }},
        { selector: 'edge.back-edge', style: {
          'line-color': '#dc2626',
          'target-arrow-color': '#dc2626',
          'line-style': 'dashed'
        }},
        { selector: 'edge.faded', style: {
          'opacity': 0.2
        }}
      ],
      layout: {
        name: 'preset',
        positions: function(ele){
          const p = positions[ele.id()];
          return p ? p : undefined;
        }
      }
    });
  };

  // FUNÇÃO PRINCIPAL: RENDERIZAR GRAFO
  
  /**
   * Função principal que renderiza o grafo completo
   * @param {Object} payload - Dados do grafo {vertices, matriz, verticeInicial}
   * @param {string} layoutName - Layout a ser usado (padrão: 'cose')
   * @returns {Object} Elementos construídos {nodes, edges, undirected}
   */
  App.renderGraph = function renderGraph(payload, layoutName = 'cose') {
    // 1. Construir nós e arestas a partir da matriz
    const elements = App.buildElements(payload);
    
    // 2. Inicializar o Cytoscape com os elementos
    App.initCy(elements, layoutName);
    
    // 3. Destacar o vértice inicial (se especificado)
    if (payload.verticeInicial) {
      const startNode = App.cy.getElementById(payload.verticeInicial);
      
      // Verificar se o nó existe
      const nodeExists = startNode && (
        typeof startNode.nonempty === 'function' 
          ? startNode.nonempty() 
          : startNode.length > 0
      );
      
      if (nodeExists) {
        // Aplicar borda mais grossa e escura no vértice inicial
        startNode.style({
          'border-width': 3,
          'border-color': '#111'
        });
      }
    }
    
    // 4. Atualizar o título da visualização com o tipo de grafo
    const headers = document.querySelectorAll('h2');
    headers.forEach(header => {
      if (header.textContent.startsWith('Visualização')) {
        const graphType = elements.undirected ? 'não direcionado' : 'direcionado';
        header.textContent = `Visualização do Grafo (${graphType})`;
      }
    });
    
    return elements;
  };

})();
