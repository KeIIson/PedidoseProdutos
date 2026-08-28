## APIs em Python para Produtor e Pedidos
import os
import json
import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

# config do boto3 SQS

SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
sqs = boto3.client("sqs", region_name=AWS_REGION)

#base de dados simulada de produto

PRODUCTS = [
    {"ID":1, "nome": "Noteook", "preco": 3700.00},
    {"ID":2, "nome": "Mouse", "preco": 50.00},
    {"ID":3, "nome": "Teclado", "preco": 150.00}
]
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API rodando na EC2!"}), 200

# Endpoint da API de Produtos
@app.route("/produtos", methods=["GET"])
def get_produtos():
    return jsonify(PRODUCTS), 200

# Endpoint da API de Pedidos
@app.route("/pedidos", methods=["POST"])
def create_pedido():
    data = request.get_json()

    if not data or "produto_id" not in data or "quantidade" not in data:
        return jsonify({"erro": "Dados inválidos. Envie 'produto_id' e 'quantidade'."}), 400

    pedido = {
        "produto_id": data["produto_id"],
        "quantidade": data["quantidade"],
        "status": "CRIADO"
    }

# Envia o pedido para a fila SQS
    try:
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(pedido)
        )
        return jsonify({
            "mensagem": "Pedido criado e enviado para a fila!",
            "message_id": response.get("MessageId")
        }), 201
    except Exception as e:
        return jsonify({"erro": f"Falha ao enviar para o SQS: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)