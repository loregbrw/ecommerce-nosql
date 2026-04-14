"""Classes de domínio.

Estas classes representam o negócio e não dependem diretamente
nem do SQLite nem do MongoDB.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass(slots=True)
class Cliente:
    id_cliente: int
    nome: str
    email: str
    cpf: str

@dataclass(slots=True)
class Endereco:
    logradouro: str
    numero: int
    bairro: str
    cidade: str
    estado: str
    cep: str

@dataclass(slots=True)
class Pagamento:
    tipo_pagamento: str
    status_pagamento: str
    valor_pago: float
    parcelas: int

@dataclass(slots=True)
class Cupom:
    id_cupom: int
    codigo: str
    tipo_desconto: str
    valor_desconto: float

@dataclass(slots=True)
class Entrega:
    status_entrega: str
    transportadora: str
    codigo_rastreio: str
    endereco: Endereco
    valor_frete: float = 0.0

@dataclass(slots=True)
class ItemPedido:
    id_produto: int
    nome: str
    quantidade: int
    sku: str
    variacao: str
    categoria: str
    preco_unitario: float = 0.0
    subtotal: float = 0.0

@dataclass(slots=True)
class Pedido:
    id_pedido: int
    data_pedido: str
    status_pedido: str
    cliente: Cliente
    cupom: Cupom
    pagamento: Optional[Pagamento]
    entrega: Optional[Entrega]
    itens: list[ItemPedido] = field(default_factory=list)
    valor_total: float = 0.0


@dataclass(slots=True)
class Vendedor:
    id_vendedor: int
    nome_loja: str
    ativo: bool

@dataclass(slots=True)
class ResumoAvaliacao:
    qtd_avaliacoes: int
    media_notas: float


@dataclass(slots=True)
class Produto:
    id_produto: int
    nome: str
    descricao: str
    preco_atual: float
    ativo: bool
    vendedor: Vendedor
    categorias: list[str] = field(default_factory=list)
    estoque_total: int = 0
    estoque_reservado: int = 0
    resumo_avaliacao: ResumoAvaliacao = field(default_factory=lambda: ResumoAvaliacao(0, 0.0))
