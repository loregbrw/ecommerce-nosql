"""Mappers entre domínio e documento MongoDB.

Nesta versão, a coleção `pedidos` foi simplificada:
- cada item do pedido vira um documento;
- o documento fica achatado;
- isso facilita os exemplos de consulta em aula.
"""

from __future__ import annotations

from src.models.domain import Pedido, Produto


class PedidoMongoMapper:
    @staticmethod
    def to_documents(pedido: Pedido) -> list[dict]:
        documentos: list[dict] = []

        cidade_entrega = None
        estado_entrega = None
        status_entrega = None
        if pedido.entrega is not None:
            cidade_entrega = pedido.entrega.endereco_snapshot.cidade
            estado_entrega = pedido.entrega.endereco_snapshot.estado
            status_entrega = pedido.entrega.status_entrega

        for indice, item in enumerate(pedido.itens, start=1):
            item_id = pedido.id_pedido * 100 + indice
            documentos.append(
                {
                    "_id": item_id,
                    "id_pedido": pedido.id_pedido,
                    "id_cliente": pedido.cliente.id_cliente,
                    "data_pedido": pedido.data_pedido,
                    "status_pedido": pedido.status_pedido,
                    "cliente_nome": pedido.cliente.nome,
                    "cliente_email": pedido.cliente.email,
                    "cidade_entrega": cidade_entrega,
                    "estado_entrega": estado_entrega,
                    "status_entrega": status_entrega,
                    "produto": item.nome_produto,
                    "categoria": item.categoria,
                    "quantidade": item.quantidade,
                    "valor_unitario": item.preco_unitario_compra,
                    "subtotal": item.subtotal,
                    "valor_total": pedido.valor_total,
                }
            )

        return documentos


class ProdutoMongoMapper:
    @staticmethod
    def to_document(produto: Produto) -> dict:
        return {
            "_id": produto.id_produto,
            "nome": produto.nome,
            "descricao": produto.descricao,
            "preco_atual": produto.preco_atual,
            "ativo": produto.ativo,
            "vendedor_nome": produto.vendedor.nome_loja,
            "categorias": produto.categorias,
            "estoque_total": produto.estoque_total,
            "media_avaliacao": produto.resumo_avaliacao.media_notas,
        }
