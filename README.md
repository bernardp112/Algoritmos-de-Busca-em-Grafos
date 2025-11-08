### Integrantes:
  * Bernardo de Souza Silva // 202108004081
  * 

### Disciplina: ANÁLISE E COMPLEXIDADE DE ALGORITMOS (IBM3121)

### Curso: Engenharia da Computação

### Professor: Cassius Figueiredo

# 🧠 Projeto: Algoritmos de Busca em Grafos (BFS e DFS) com API Flask

Este projeto implementa dois algoritmos clássicos de busca em grafos — **BFS (Busca em Largura)** e **DFS (Busca em Profundidade)** — com uma **API Flask** que permite executar ambos via requisições HTTP, além de um script de teste para uso local.

---

## 📁 Estrutura do Projeto

├── app.py # Servidor Flask com rotas /bfs e /dfs
├── bfs.py # Implementação do algoritmo BFS
├── dfs.py # Implementação do algoritmo DFS
├── teste.py # Script de teste local (sem servidor)
├── requirements.txt # Dependências do projeto


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

1. **Rodar o servidor Flask**

Execute o comando:

  ```bash
  python app.py
  ```

O servidor será iniciado em:

  ```bash
  http://127.0.0.1:5000
  ```

2. **Testar a rota /bfs**

  Requisição:
    ```bash
    curl -X GET http://127.0.0.1:5000/bfs \
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
    
3. **Testar a rota /dfs**
   
  Requisição:
    ```bash
    curl -X GET http://127.0.0.1:5000/dfs \
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

4. **Testar localmente sem o servidor**

   Você pode apenas executar:
     ```bash
      python teste.py
     ```
   Esse script executa as funções BFS e DFS diretamente e exibe os resultados no terminal.

---

## 🧩 Descrição dos arquivos

| Arquivo                | Descrição                                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **`app.py`**           | Servidor Flask com duas rotas GET (`/bfs` e `/dfs`) que processam o grafo e retornam os resultados em JSON.                                 |
| **`bfs.py`**           | Implementação do algoritmo **Busca em Largura (Breadth-First Search)**, retornando componentes, árvore BFS e níveis dos vértices.           |
| **`dfs.py`**           | Implementação do algoritmo **Busca em Profundidade (Depth-First Search)**, incluindo tempos de descoberta/finalização e arestas de retorno. |
| **`teste.py`**         | Script de teste para rodar localmente e verificar o comportamento dos algoritmos sem precisar da API.                                       |
| **`requirements.txt`** | Lista das dependências mínimas para rodar o projeto (`flask` e `collections`).                                                              |

--

## 🧪 Tecnologias utilizadas

* Python 3
* Flask (API REST)
* Collections (deque)
