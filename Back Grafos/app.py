from flask import Flask, request, jsonify
from bfs import bfs
from dfs import dfs_com_tempos

app = Flask(__name__)

@app.route("/dfs", methods=["GET"])
def dfs_route():
    """
    Rota que executa a busca em profundidade (DFS).
    Espera um JSON com os dados do grafo.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Corpo da requisição deve conter um JSON válido."}), 400

        tempos, arvore, retorno = dfs_com_tempos(data)

        response = {
            "tempos": tempos,
            "arvore": arvore,
            "arestas_retorno": retorno
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/bfs", methods=["GET"])
def bfs_route():
    """
    Rota que executa a busca em largura (BFS).
    Espera um JSON com os dados do grafo.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Corpo da requisição deve conter um JSON válido."}), 400

        ordem, niveis = bfs(data)

        response = {
            "ordem": ordem,
            "niveis": niveis
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
