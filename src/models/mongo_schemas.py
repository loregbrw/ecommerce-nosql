"""Schemas de validação do MongoDB.

Nesta versão, o modelo documental foi simplificado de propósito
para servir como ponto de partida para os grupos adaptarem.

Ideia principal da coleção `pedidos`:
- um documento por item do pedido;
- documento mais achatado;
- fácil de consultar em aula com filtros, projeções, updates,
  agregação e paginação.
"""

from __future__ import annotations


def pedido_validator() -> dict:
    """Schema simplificado da coleção pedidos.

    Observação didática:
    - `_id` usa o id do item do pedido;
    - `id_pedido` permite agrupar itens do mesmo pedido;
    - vários campos foram achatados para facilitar a leitura.
    """
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "_id",
                "data_pedido",
                "status_pedido",
                "cliente_nome",
                "produto",
                "quantidade",
                "valor_total",
            ],
            "properties": {
                "_id": {"bsonType": ["int", "long"]},
                "id_pedido": {"bsonType": ["int", "long"]},
                "id_cliente": {"bsonType": ["int", "long"]},
                "data_pedido": {"bsonType": "string"},
                "status_pedido": {
                    "enum": ["pendente", "pago", "cancelado", "entregue"]
                },
                "cliente_nome": {"bsonType": "string"},
                "cliente_email": {"bsonType": "string"},
                "cidade_entrega": {"bsonType": ["string", "null"]},
                "estado_entrega": {"bsonType": ["string", "null"]},
                "status_entrega": {"bsonType": ["string", "null"]},
                "produto": {"bsonType": "string"},
                "categoria": {"bsonType": ["string", "null"]},
                "quantidade": {
                    "bsonType": ["int", "long"],
                    "minimum": 1,
                },
                "valor_unitario": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0,
                },
                "subtotal": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0,
                },
                "valor_total": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0,
                },
            },
        }
    }


def produto_validator() -> dict:
    """Schema simplificado da coleção produtos."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "nome", "preco_atual", "ativo"],
            "properties": {
                "_id": {"bsonType": ["int", "long"]},
                "nome": {"bsonType": "string"},
                "descricao": {"bsonType": "string"},
                "preco_atual": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0,
                },
                "ativo": {"bsonType": "bool"},
                "vendedor_nome": {"bsonType": "string"},
                "categorias": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                },
                "estoque_total": {"bsonType": ["int", "long"], "minimum": 0},
                "media_avaliacao": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0,
                },
            },
        }
    }
