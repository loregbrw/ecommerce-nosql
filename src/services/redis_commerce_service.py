"""Serviços de negócio para cache, carrinho e ranking com Redis."""

from __future__ import annotations

import json

from src.models.redis_manager import RedisManager
from src.models.sqlite_repository import SQLiteRepository


class RedisCommerceService:
    def __init__(
        self,
        repository: SQLiteRepository,
        redis_manager: RedisManager,
        key_prefix: str,
        product_cache_ttl_seconds: int,
        cart_ttl_seconds: int,
    ) -> None:
        self.repository = repository
        self.redis = redis_manager
        self.key_prefix = key_prefix
        self.product_cache_ttl_seconds = product_cache_ttl_seconds
        self.cart_ttl_seconds = cart_ttl_seconds

    def consultar_produto_por_id(self, id_produto: int) -> dict | None:
        client = self.redis.ensure_connected()
        cache_key = self._product_cache_key(id_produto)
        cache_value = client.get(cache_key)

        if cache_value:
            produto = json.loads(cache_value)
            self._incrementar_ranking(client, id_produto)
            produto["origem"] = "redis-cache"
            return produto

        produto = self.repository.get_produto_resumo_by_id(id_produto)
        if produto is None:
            return None

        client.setex(cache_key, self.product_cache_ttl_seconds, json.dumps(produto))
        self._incrementar_ranking(client, id_produto)
        produto["origem"] = "sqlite"
        return produto

    def adicionar_ao_carrinho(self, id_cliente: int, id_produto: int, quantidade: int) -> tuple[bool, str]:
        if quantidade <= 0:
            return False, "A quantidade deve ser maior que zero."
        if not self.repository.cliente_exists(id_cliente):
            return False, f"Cliente {id_cliente} não encontrado."

        produto = self.repository.get_produto_resumo_by_id(id_produto)
        if produto is None:
            return False, f"Produto {id_produto} não encontrado."

        client = self.redis.ensure_connected()
        cart_key = self._cart_key(id_cliente)
        quantidade_atual = int(client.hget(cart_key, str(id_produto)) or 0)
        nova_quantidade = quantidade_atual + quantidade

        if nova_quantidade > produto["estoque"]:
            return (
                False,
                f"Estoque insuficiente para o produto {id_produto}. "
                f"Disponível: {produto['estoque']}, solicitado no carrinho: {nova_quantidade}.",
            )

        client.hset(cart_key, str(id_produto), nova_quantidade)
        client.expire(cart_key, self.cart_ttl_seconds)
        return True, "Produto adicionado ao carrinho temporário."

    def visualizar_carrinho(self, id_cliente: int) -> dict:
        if not self.repository.cliente_exists(id_cliente):
            raise ValueError(f"Cliente {id_cliente} não encontrado.")

        client = self.redis.ensure_connected()
        cart_key = self._cart_key(id_cliente)
        cart_data = client.hgetall(cart_key)
        if not cart_data:
            return {"id_cliente": id_cliente, "itens": [], "valor_total": 0.0}

        ids_produto = sorted(int(id_produto) for id_produto in cart_data.keys())
        produtos = self.repository.get_produtos_resumo_by_ids(ids_produto)

        itens = []
        valor_total = 0.0
        for id_produto_str, quantidade_str in cart_data.items():
            id_produto = int(id_produto_str)
            quantidade = int(quantidade_str)
            produto = produtos.get(id_produto)
            if produto is None:
                continue

            subtotal = round(produto["preco"] * quantidade, 2)
            valor_total += subtotal
            itens.append(
                {
                    "id_produto": id_produto,
                    "nome": produto["nome"],
                    "preco": produto["preco"],
                    "quantidade": quantidade,
                    "subtotal": subtotal,
                }
            )

        client.expire(cart_key, self.cart_ttl_seconds)
        return {"id_cliente": id_cliente, "itens": itens, "valor_total": round(valor_total, 2)}

    def ranking_produtos_mais_consultados(self, limit: int = 10) -> list[dict]:
        client = self.redis.ensure_connected()
        ranking = client.zrevrange(self._ranking_key(), 0, limit - 1, withscores=True)
        if not ranking:
            return []

        ids_produto = [int(id_produto) for id_produto, _ in ranking]
        produtos = self.repository.get_produtos_resumo_by_ids(ids_produto)

        resultado = []
        for id_produto_str, consultas in ranking:
            id_produto = int(id_produto_str)
            produto = produtos.get(id_produto)
            if produto is None:
                continue
            resultado.append(
                {
                    "id_produto": id_produto,
                    "nome": produto["nome"],
                    "preco": produto["preco"],
                    "consultas": int(consultas),
                }
            )
        return resultado

    def _incrementar_ranking(self, client, id_produto: int) -> None:
        client.zincrby(self._ranking_key(), 1, str(id_produto))

    def _product_cache_key(self, id_produto: int) -> str:
        return f"{self.key_prefix}:produto:cache:{id_produto}"

    def _cart_key(self, id_cliente: int) -> str:
        return f"{self.key_prefix}:carrinho:cliente:{id_cliente}"

    def _ranking_key(self) -> str:
        return f"{self.key_prefix}:ranking:produtos:consultas"
