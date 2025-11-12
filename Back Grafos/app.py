from flask import Flask, request, jsonify, render_template
from bfs import bfs
from dfs import dfs_com_tempos
from visualizacao_ascii import gerar_ascii_bfs, gerar_ascii_dfs

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dfs", methods=["GET", "POST"])
def dfs_route():
    """
    Rota que executa a busca em profundidade (DFS).
    Espera um JSON com os dados do grafo.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"erro": "Corpo da requisição deve conter um JSON válido."}), 400

        tempos, arvore, retorno = dfs_com_tempos(data)
        
        # Verificar se o grafo é direcionado (matriz não simétrica)
        matriz = data.get("matriz", [])
        vertices = data.get("vertices", [])
        is_directed = not is_symmetric(matriz)
        
        # Gerar visualização ASCII
        ascii_output = gerar_ascii_dfs(tempos, arvore, retorno, is_directed, matriz, vertices)

        response = {
            "tempos": tempos,
            "arvore": arvore,
            "arestas_retorno": retorno,
            "ascii": ascii_output
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def is_symmetric(matriz):
    """Verifica se a matriz de adjacência é simétrica (grafo não direcionado)"""
    n = len(matriz)
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != matriz[j][i]:
                return False
    return True


@app.route("/bfs", methods=["GET", "POST"])
def bfs_route():
    """
    Rota que executa a busca em largura (BFS).
    Espera um JSON com os dados do grafo.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"erro": "Corpo da requisição deve conter um JSON válido."}), 400

        ordem, niveis = bfs(data)
        
        # Gerar visualização ASCII
        ascii_output = gerar_ascii_bfs(ordem, niveis)

        response = {
            "ordem": ordem,
            "niveis": niveis,
            "ascii": ascii_output
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
