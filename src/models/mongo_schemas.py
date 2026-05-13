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
                "cliente",
                "itens",
                "valor_total"
            ],
            "properties": {
                "_id": {"bsonType": ["int", "long"]},
                "data_pedido": {"bsonType": "string"},
                "status_pedido": {
                    "enum": ["pendente", "pago", "cancelado", "entregue"]
                },
                "cliente": {
                    "bsonType": "object",
                    "required": ["id_cliente", "nome", "email"],
                    "properties": {
                        "id_cliente": {"bsonType": ["int", "long"]},
                        "nome": {"bsonType": "string"},
                        "email": {"bsonType": "string"},
                    }
                },
                "itens": {
                    "bsonType": "array",
                    "minItems": 1,
                    "items": {
                        "bsonType": "object",
                        "required": ["id_produto", "nome_produto_snapshot", "quantidade", "preco_unitario_compra"],
                        "properties": {
                            "id_produto": {"bsonType": ["int", "long"]},
                            "nome_produto_snapshot": {"bsonType": "string"},
                            "sku_snapshot": {"bsonType": "string"},
                            "variacao_snapshot": {"bsonType": "string"},
                            "categoria_snapshot": {"bsonType": "string"},
                            "quantidade": {"bsonType": ["int", "long"], "minimum": 1},
                            "preco_unitario_compra": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0},
                            "subtotal": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0}
                        }
                    }
                },
                "pagamento": {
                    "bsonType": "object",
                    "properties": {
                        "tipo_pagamento": {"enum": ["cartao", "pix", "boleto"]},
                        "status_pagamento": {"enum": ["pendente", "aprovado", "recusado"]},
                        "valor": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0},
                        "parcelas": { "bsonType": "int" }
                    }
                },
                "entrega": {
                    "bsonType": "object",
                    "properties": {
                        "status_entrega": {"enum": ["pendente", "em_transporte", "entregue"]},
                        "transportadora": {"bsonType": "string"},
                        "codigo_rastreio": {"bsonType": "string"},
                        "endereco": {
                            "bsonType": "object",
                            "properties": {
                                "logradouro": {"bsonType": "string"},
                                "numero": {"bsonType": "string"},
                                "bairro": {"bsonType": "string"},
                                "cidade": {"bsonType": "string"},
                                "estado": {"bsonType": "string"},
                                "cep": {"bsonType": "string"}
                            }
                        }
                    }
                },
                "valor_total": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0}
            }
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
            }
        }
    }
