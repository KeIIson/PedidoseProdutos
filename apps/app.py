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
    {"ID":3, "nome": "Teclado", "preco": 150,00}
]