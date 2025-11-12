// ============================================
// MAIN.JS - Lógica Principal da Interface
// ============================================

(function() {
  // Funções auxiliares para selecionar elementos DOM
  const getElement = (selector) => document.querySelector(selector);
  const getAllElements = (selector) => document.querySelectorAll(selector);
  
  // Namespace global da aplicação
  const App = window.App = window.App || {};

  // ============================================
  // GERENCIAMENTO DE ABAS
  // ============================================
  
  /**
   * Troca entre as abas "Inserir Grafo" e "Visualizar Grafo"
   * @param {string} tabName - Nome da aba ('input' ou 'graph')
   */
  function switchTab(tabName) {
    // Remove a classe 'active' de todos os botões e conteúdos
    getAllElements('.tab-button').forEach(button => {
      button.classList.remove('active');
    });
    
    getAllElements('.tab-content').forEach(content => {
      content.classList.remove('active');
    });
    
    // Adiciona 'active' na aba selecionada
    const selectedButton = getElement(`.tab-button[data-tab="${tabName}"]`);
    const selectedContent = getElement(`#${tabName}-tab`);
    
    selectedButton.classList.add('active');
    selectedContent.classList.add('active');
    
    // Se abriu a aba do grafo, renderiza automaticamente
    if (tabName === 'graph') {
      try {
        const graphData = App.readPayload();
        App.renderGraph(graphData);
      } catch (error) {
        console.error('Erro ao renderizar grafo:', error);
      }
    }
  }

  // Adiciona event listeners para todos os botões de aba
  getAllElements('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
      const tabName = button.getAttribute('data-tab');
      switchTab(tabName);
    });
  });

  // ============================================
  // CHAMADAS À API (BFS/DFS)
  // ============================================
  
  /**
   * Faz uma chamada POST para o endpoint da API
   * @param {string} endpoint - Rota da API ('/bfs' ou '/dfs')
   */
  async function callAPI(endpoint) {
    const outputElement = getElement("#output");
    const asciiOutputElement = getElement('#ascii-output');
    
    // 1. Ler o JSON do textarea
    let graphData;
    try {
      graphData = App.readPayload();
    } catch (error) {
      // Se o JSON for inválido, readPayload já mostra o erro
      return;
    }
    
    // 2. Mostrar "Enviando..." enquanto aguarda resposta
    outputElement.textContent = "Enviando requisição...";
    asciiOutputElement.style.display = 'none';
    
    try {
      // 3. Fazer requisição POST para a API
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(graphData)
      });
      
      // 4. Pegar resposta como texto
      const responseText = await response.text();
      
      // 5. Tentar converter para JSON
      let responseData;
      try {
        responseData = JSON.parse(responseText);
      } catch (jsonError) {
        // Se não for JSON válido, mostrar o texto bruto
        outputElement.textContent = responseText;
        return;
      }
      
      // 6. Mostrar JSON formatado na seção "Resposta JSON"
      outputElement.textContent = JSON.stringify(responseData, null, 2);
      
      // 7. Se tiver visualização ASCII, mostrar
      if (responseData.ascii) {
        asciiOutputElement.textContent = responseData.ascii;
        asciiOutputElement.style.display = 'block';
      }
      
    } catch (networkError) {
      outputElement.textContent = 'Erro de rede: ' + networkError.message;
    }
  }

  // ============================================
  // EVENT LISTENERS DOS BOTÕES
  // ============================================
  
  getElement('#btnBFS').addEventListener('click', () => {
    callAPI('/bfs');
  });
  
  getElement('#btnDFS').addEventListener('click', () => {
    callAPI('/dfs');
  });

})();
