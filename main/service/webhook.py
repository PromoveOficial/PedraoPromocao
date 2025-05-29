from flask import Flask, request
from pyngrok import ngrok

# Inicia a aplicação Flask
app = Flask(__name__)

# Define uma rota para receber requisições POST e GET
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        print("Recebido (POST):", data)
        return "POST recebido", 200
    else:
        return "GET OK", 200

# Cria o túnel ngrok para a porta 5000
public_url = ngrok.connect(5000)
print(f"Túnel ngrok ativo em: {public_url}/webhook")

# Inicia o servidor Flask
app.run(port=5000)