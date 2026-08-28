import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Processa mensagens vindas da fila SQS 'pedidos-a-processar'."""
    for record in event.get('Records', []):
        body = record.get('body', '')
        logger.info(f"--- NOVO PEDIDO RECEBIDO DA FILA SQS ---")
        logger.info(f"Conteúdo do Pedido: {body}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso!')
    }