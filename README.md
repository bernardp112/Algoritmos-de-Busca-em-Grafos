### Integrantes:
  * Bernardo de Souza Silva // 202108004081
  * Murilo Plombon Piatigorsky // 202202448605

### Disciplina: ANÁLISE E COMPLEXIDADE DE ALGORITMOS (IBM3121)

### Curso: Engenharia da Computação

### Professor: Cassius Figueiredo

---

# 🧠 Projeto: Algoritmos de Busca em Grafos (BFS e DFS) com API Flask

Este projeto implementa dois algoritmos clássicos de busca em grafos — **BFS (Busca em Largura)** e **DFS (Busca em Profundidade)** — com uma **API Flask** e uma **interface web interativa** que permite:
- Inserir grafos via JSON
- Visualizar o grafo renderizado com Cytoscape.js
- Executar BFS/DFS e ver a execução passo a passo em formato ASCII
- Visualizar arestas de retorno (back edges) e estrutura de árvore

---

## 📁 Estrutura do Projeto

```
Back Grafos/
├── app.py                      # Servidor Flask com rotas /bfs, /dfs e /
├── bfs.py                      # Implementação do algoritmo BFS
├── dfs.py                      # Implementação do algoritmo DFS
├── visualizacao_ascii.py       # Geração de visualizações ASCII para BFS/DFS
├── teste.py                    # Script de teste local (sem servidor)
├── requirements.txt            # Dependências do projeto
├── templates/
│   └── index.html             # Interface web principal
└── static/
    ├── css/
    │   └── style.css          # Estilos da interface
    └── js/
        ├── main.js            # Lógica principal e gerenciamento de abas
        └── graph.js           # Renderização do grafo com Cytoscape.js
```

---

## ⚙️ Pré-requisitos

Certifique-se de ter instalado:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

---

## 📦 Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
  
2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. **Instale as dependências**
   
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Execução

### Opção 1: Interface Web (Recomendado)

1. **Rodar o servidor Flask**

   ```bash
   cd "Back Grafos"
   python app.py
   ```

   O servidor será iniciado em:
   
   ```
   http://127.0.0.1:5000
   ```

2. **Acessar a interface web**

   Abra o navegador e acesse `http://127.0.0.1:5000`
   
   **Funcionalidades da interface:**
   - **Aba "Inserir Grafo"**: Edite o JSON do grafo e execute BFS/DFS
   - **Aba "Visualizar Grafo"**: Veja o grafo renderizado com Cytoscape.js
   - **Execução ASCII**: Visualização passo a passo da execução dos algoritmos
   - **Resposta JSON**: Dados completos retornados pela API

### Opção 2: API via cURL/Postman

1. **Testar a rota /bfs**

   Requisição POST:
   ```bash
   curl -X POST http://127.0.0.1:5000/bfs \
          -H "Content-Type: application/json" \
          -d '{
               "vertices": ["A","B","C","D","E","F","G","H","I","J"],
               "verticeInicial": "B",
               "matriz": [
                   [0,0,0,1,1,1,0,0,0,1],
                   [0,0,1,0,1,0,0,0,0,0],
                   [0,1,0,0,1,0,0,0,0,0],
                   [1,0,0,0,1,0,0,0,0,0],
                   [1,1,1,1,0,1,0,0,0,0],
                   [1,0,0,0,1,0,0,0,0,1],
                   [0,0,0,0,0,0,0,1,1,0],
                   [0,0,0,0,0,0,1,0,1,0],
                   [0,0,0,0,0,0,1,1,0,0],
                   [1,0,0,0,0,1,0,0,0,0]
               ]
           }'
    ```
   Resposta esperada (exemplo):
    ```bash
     {
         "niveis": {
             "A": 2,
             "B": 0,
             "C": 1,
             "D": 2,
             "E": 1,
             "F": 2,
             "G": 0,
             "H": 1,
             "I": 1,
             "J": 3
         },
         "ordem": [
             [
                 "B",
                 "C",
                 "E",
                 "A",
                 "D",
                 "F",
                 "J"
             ],
             [
                 "G",
                 "H",
                 "I"
             ]
         ]
     }
    ```
    
2. **Testar a rota /dfs**
   
   Requisição POST:
   ```bash
   curl -X POST http://127.0.0.1:5000/dfs \
          -H "Content-Type: application/json" \
          -d '{
               "vertices": ["A","B","C","D","E","F","G","H","I","J"],
               "verticeInicial": "B",
               "matriz": [
                   [0,0,0,1,1,1,0,0,0,1],
                   [0,0,1,0,1,0,0,0,0,0],
                   [0,1,0,0,1,0,0,0,0,0],
                   [1,0,0,0,1,0,0,0,0,0],
                   [1,1,1,1,0,1,0,0,0,0],
                   [1,0,0,0,1,0,0,0,0,1],
                   [0,0,0,0,0,0,0,1,1,0],
                   [0,0,0,0,0,0,1,0,1,0],
                   [0,0,0,0,0,0,1,1,0,0],
                   [1,0,0,0,0,1,0,0,0,0]
               ]
           }'
     ```
   Resposta esperada (exemplo):
     ```bash
     {
         "arestas_retorno": [
             [
                 "D",
                 "E"
             ],
             [
                 "F",
                 "E"
             ],
             [
                 "J",
                 "A"
             ],
             [
                 "E",
                 "B"
             ],
             [
                 "I",
                 "G"
             ]
         ],
         "arvore": [
             [
                 "B",
                 "C"
             ],
             [
                 "C",
                 "E"
             ],
             [
                 "E",
                 "A"
             ],
             [
                 "A",
                 "D"
             ],
             [
                 "A",
                 "F"
             ],
             [
                 "F",
                 "J"
             ],
             [
                 "G",
                 "H"
             ],
             [
                 "H",
                 "I"
             ]
         ],
         "tempos": {
             "A": {
                 "descoberta": 4,
                 "finalizacao": 11
             },
             "B": {
                 "descoberta": 1,
                 "finalizacao": 14
             },
             "C": {
                 "descoberta": 2,
                 "finalizacao": 13
             },
             "D": {
                 "descoberta": 5,
                 "finalizacao": 6
             },
             "E": {
                 "descoberta": 3,
                 "finalizacao": 12
             },
             "F": {
                 "descoberta": 7,
                 "finalizacao": 10
             },
             "G": {
                 "descoberta": 15,
                 "finalizacao": 20
             },
             "H": {
                 "descoberta": 16,
                 "finalizacao": 19
             },
             "I": {
                 "descoberta": 17,
                 "finalizacao": 18
             },
             "J": {
                 "descoberta": 8,
                 "finalizacao": 9
             }
         }
     }
    ```

### Opção 3: Teste Local (sem servidor)

Você pode executar os algoritmos diretamente:

```bash
cd "Back Grafos"
python teste.py
```

Esse script executa as funções BFS e DFS diretamente e exibe os resultados no terminal.

---

## 🧩 Descrição dos arquivos

| Arquivo                      | Descrição                                                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`app.py`**                 | Servidor Flask com rotas POST (`/bfs` e `/dfs`) que processam o grafo e retornam resultados em JSON + ASCII. Rota GET `/` serve a interface.   |
| **`bfs.py`**                 | Implementação do algoritmo **Busca em Largura (Breadth-First Search)**, retornando ordem da visita e níveis dos vértices.                       |
| **`dfs.py`**                 | Implementação do algoritmo **Busca em Profundidade (Depth-First Search)**, incluindo tempos de descoberta/finalização e arestas de retorno.     |
| **`visualizacao_ascii.py`**  | Gera visualizações ASCII dos algoritmos: BFS exibe ordem de execução `[A0, B1, ...]`, DFS exibe árvore com conectores `├──` e arestas de retorno inline. |
| **`teste.py`**               | Script de teste para rodar localmente e verificar o comportamento dos algoritmos sem precisar da API.                                           |
| **`requirements.txt`**       | Lista das dependências do projeto.                                                                                                               |
| **`templates/index.html`**   | Interface web com abas para inserir grafo e visualizar renderização.                                                                             |
| **`static/css/style.css`**   | Estilos da interface com suporte a tema claro/escuro.                                                                                            |
| **`static/js/main.js`**      | Gerenciamento de abas, chamadas à API e exibição de resultados.                                                                                 |
| **`static/js/graph.js`**     | Renderização do grafo usando Cytoscape.js, com detecção automática de grafos direcionados/não-direcionados.                                     |

---

## 🎨 Funcionalidades da Interface

### Visualização ASCII do DFS
- Árvore hierárquica com conectores unicode (`├──`, `└──`, `│`)
- Tempos de descoberta e finalização: `S(1/12)`
- Detecção de arestas bidirecionais (sem seta: `├──`) vs unidirecionais (com seta: `├──>`)
- Arestas de retorno exibidas inline com `↖ Retorno para X`

### Visualização ASCII do BFS
- Ordem de execução por nível: `[S0, A1, D1, B2, E2, C3]`
- Formato compacto mostrando vértice + nível

### Renderização Gráfica
- Grafo renderizado com Cytoscape.js
- Detecção automática de grafos direcionados (mostra setas) vs não-direcionados
- Layout circular para melhor visualização

---

## 🧪 Tecnologias utilizadas

* **Backend**: Python 3.8+, Flask
* **Frontend**: HTML5, CSS3 (com variáveis CSS para temas), JavaScript (Vanilla)
* **Visualização**: Cytoscape.js 3.28.1
* **Estruturas de Dados**: Collections (deque)
