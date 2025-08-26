from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simulação de banco de dados em memória
produtos = {
    "Batata inglesa 10 kg": {"quantidade": 172, "preco": 20.00},
    "Cebola nacional 10 kg": {"quantidade": 216, "preco": 20.00},
    "Cebola roxa 20 kg": {"quantidade": 12, "preco": 30.00},
    "Cebola nacional 20 kg": {"quantidade": 12, "preco": 30.00},
    "Alho 2kg": {"quantidade": 27, "preco": 30.00},
    "Alho 20kg": {"quantidade": 2, "preco": 200.00}
}

pendencias = []
vendas = {"dinheiro": 0.0, "debito": 0.0, "credito": 0.0, "pix": 0.0}
caixa_inicial = 200.0  # Troco inicial
caixa_total = caixa_inicial

@app.route("/")
def index():
    return render_template("index.html", produtos=produtos, caixa=caixa_total, vendas=vendas, pendencias=pendencias, caixa_inicial=caixa_inicial)

@app.route("/saida", methods=["POST"])
def saida():
    global caixa_total
    produto = request.form["produto"]
    quantidade = int(request.form["quantidade"])
    pagamento = request.form["pagamento"]

    if produto in produtos and produtos[produto]["quantidade"] >= quantidade:
        produtos[produto]["quantidade"] -= quantidade
        valor_venda = produtos[produto]["preco"] * quantidade
        caixa_total += valor_venda
        vendas[pagamento] += valor_venda
    return redirect(url_for("index"))

@app.route("/entrada", methods=["POST"])
def entrada():
    produto = request.form["produto"]
    quantidade = int(request.form["quantidade"])
    if produto in produtos:
        produtos[produto]["quantidade"] += quantidade
    return redirect(url_for("index"))

@app.route("/pendencia", methods=["POST"])
def pendencia():
    cliente = request.form["cliente"]
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    data = datetime.now().strftime("%d/%m/%Y")
    pendencias.append({"cliente": cliente, "descricao": descricao, "quantidade": quantidade, "data": data, "buscou": False})
    return redirect(url_for("index"))

@app.route("/pendencia/buscar/<int:index>")
def buscar_pendencia(index):
    if 0 <= index < len(pendencias):
        pendencias[index]["buscou"] = True
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
