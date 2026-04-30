def schema_pedido():
    """Define o schema mínimo da coleção."""
    return {
            "$jsonSchema": {
                "bsonType": "object",
                "required": [
                    "_id",
                    "data_pedido",
                    "status_pedido",
                    "cliente",
                    "itens",
                    "entrega",
                    "pagamentos"
                ],
                "properties": {
                    "_id": {
                        "bsonType": [ "int", "long" ]
                    },
                    "data_pedido": {
                        "bsonType": "string"
                    },
                    "status_pedido": {
                        "enum": ["pendente", "pago", "cancelado", "entregue", "preparando"]
                    },

                    "cliente": {
                        "bsonType": "object",
                        "required": [
                            "id_cliente",
                            "nome",
                            "email"
                        ],
                        "properties": {
                            "id_cliente": {
                                "bsonType": [ "int", "long" ]
                            },
                            "nome": {
                                "bsonType": "string"
                            },
                            "email": {
                                "bsonType": "string"
                            }
                        }
                    },

                    "itens": {
                        "bsonType": "array",
                        "minItems": 1,
                        "items": {
                            "bsonType": "object",
                            "required": [
                                "id_produto",
                                "quantidade",
                                "preco_unitario",
                                "nome_produto",
                                "subtotal"
                            ],
                            "properties": {
                                "id_produto": {
                                    "bsonType": [ "int", "long "]
                                },
                                "quantidade": {
                                    "bsonType": [ "int", "long", "double" ],
                                    "minimum": 1
                                },
                                "preco_unitario": {
                                    "bsonType": [ "double", "decimal", "int" ],
                                    "minimum": 0
                                },
                                "nome_produto": {
                                    "bsonType": "string"
                                },
                                "subtotal": {
                                    "bsonType": [ "double", "int", "long", "decimal" ],
                                    "minimum": 0
                                }
                            }
                        }
                    },

                    "entrega": {
                        "bsonType": "object",
                        "required": [
                            "cep",
                            "logradouro",
                            "numero",
                            "status_entrega"
                        ],
                        "properties": {
                            "cep": {
                                "bsonType": "string"
                            },
                            "logradouro": {
                                "bsonType": "string"
                            },
                            "numero": {
                                "bsonType": "string"
                            },
                            "status_entrega": {
                                "enum": [ "entregue", "caminho", "preparando" ]
                            }
                        }
                    },

                    "pagamentos": {
                        "bsonType": "object",
                        "required": [
                            "tipo_pagamento",
                            "status_pagamento",
                            "parcelas",
                            "valor"
                        ],
                        "properties": {
                            "tipo_pagamento": {
                                "enum": [ "dinheiro", "pix", "crédito", "boleto" ]
                            },
                            "status_pagamento": {
                                "enum": [ "pendente", "concluido", "cancelado" ], 
                            },
                            "parcelas": {
                                "bsonType": "int",
                                "minimum": 0
                            },
                            "valor": {
                                "bsonType": [ "double", "decimal", "int" ],
                                "minimum": 0
                        }
                    },
                    "valor_total": {
                        "bsonType": [ "double", "decimal", "int" ],
                        "minimum": 0
                    },
                }
            }
        }
