# ecommerce-nosql

Projeto acadêmico de **Banco de Dados Não Relacionais** com backend em Python, usando SQLite/MongoDB e extensão com Redis para:
- cache de produto por ID;
- carrinho temporário por cliente;
- ranking de produtos mais consultados.

## Requirements

- Python 3.11+  
- Pip  
- Docker Desktop (para MongoDB/Redis/RedisInsight via compose)
- Dependências Python em `requirements.txt`

## Como rodar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. (Opcional, recomendado) Suba os serviços de banco:

```bash
docker compose -f DockerCompose\compose.yaml up -d
```

3. Execute a aplicação:

```bash
python main.py
```

4. No menu do terminal, use as opções para recriar base, testar conexões e executar as demandas com Redis.
