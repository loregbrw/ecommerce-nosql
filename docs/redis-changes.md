# Atividade - Especificação de Mudança com Redis
Banco de Dados Não Relacionais | Projeto base com Redis

## 4. Documento de especificação da mudança

### 4.1 Identificação

**Grupo:** XGH  
**Integrantes:** Adrian Falci, Lorena Falci, Douglas e Nilton

### 4.2 Análise das demandas

- **Demanda 1 (Consulta de Produtos):** Resolve o problema de latência e sobrecarga no banco de dados principal (SQL). Através do cache, evita-se consultas repetitivas a dados que mudam com pouca frequência.
- **Demanda 2 (Carrinho Temporário):** Resolve o problema de persistência desnecessária de dados voláteis. Evita "lixo" no banco SQL caso o cliente desista da compra, mantendo a performance para dados em rascunho.
- **Demanda 3 (Ranking de Consultas):** Resolve o problema de processamento pesado de agregação (COUNT/GROUP BY) no SQL. Fornece métricas em tempo real sobre o comportamento do usuário com baixo custo computacional.

### 4.3 Técnica Redis escolhida

- **Demanda 1: String com JSON + TTL.** Escolhida por ser a forma mais eficiente de serializar um objeto completo do banco e recuperá-lo integralmente em uma única operação de I/O.
- **Demanda 2: Hash + TTL.** Escolhida porque um carrinho possui múltiplos sub-itens (produtos e quantidades). O Hash permite manipular campos específicos (como alterar a quantidade de um único item) sem precisar reescrever todo o objeto.
- **Demanda 3: Sorted Set (ZSET).** Escolhida especificamente para rankings. O Redis gerencia nativamente a ordenação conforme incrementamos o score (número de consultas), permitindo recuperar o "Top N" de forma instantânea.


### 4.4 Padrão das chaves Redis

`ecommerce:produto:cache:{id}`
- **Representa:** Cache individual de um produto.
- **Dado:** Objeto JSON com nome, preço e estoque.
- **TTL:** Sim (ex: 3600 segundos).

`ecommerce:carrinho:{session_id}`
- **Representa:** O carrinho ativo de um usuário.
- **Dado:** Mapeamento de id_produto -> quantidade.
- **TTL:** Sim (ex: 1800 segundos após última interação).

`ecommerce:ranking:consultas`
- **Representa:** O ranking global de interesse.
- **Dado:** Sorted Set onde o member é o ID do produto e o score é o contador.
- **TTL:** Não (permanente para análise de longo prazo).

### 4.5 Relação entre Redis e SQL

| Demanda | Origem SQL | Armazenamento Redis | Função do Redis |
|---|---|---|---|
| 1 | Dados mestres do produto. | Cópia serializada (JSON). | Cache (Read-aside). |
| 2 | Validação de estoque e existência. | IDs e quantidades temporárias. | Armazenamento Efêmero. |
| 3 | Nome e preço para exibição final. | IDs e pontuação de consultas. | Estrutura de Apoio (Analytics). |


### 4.6 Mudanças no projeto base

Preencher uma tabela simples:

| Parte do projeto | Alteração prevista |
|---|---|
| docker-compose.yml | Adição da imagem redis:alpine e mapeamento da porta 6379. |
| requirements.txt | Inclusão da biblioteca redis. |
| Menu/Terminal | Novas opções: "Ver Carrinho", "Adicionar ao Carrinho" e "Ver Ranking". |
| Controller | Chamada de lógica para gerenciar sessão e fluxo de dados Redis/SQL. |
| Service | Implementação das regras: verificar cache antes do SQL; atualizar ranking no "get_by_id". |
| Repository/SQL | Mantido como fonte da verdade, sem alterações estruturais |
| Configuração Redis | Criação de um redis_client.py para gerenciar a conexão via variáveis de ambiente. |


### 4.7 Plano de implementação

- **Infraestrutura:** Subir o container Redis e configurar a conexão no Python.
- **Camada de Cache (D1):** Alterar o método de busca de produto para verificar o Redis antes do banco SQL. Implementar o setex para o TTL.
- **Contador de Ranking (D3):** No mesmo método de busca, disparar o comando ZINCRBY caso o produto exista.
- **Gestão de Carrinho (D2):** Criar os métodos de hset (adicionar) e hgetall (visualizar), garantindo a checagem de estoque no SQL antes da inserção no Redis.


### 4.8 Testes previstos

- **Teste de Cache:** Consultar o mesmo produto duas vezes e verificar via log (ou RedisInsight) que a segunda consulta não disparou SELECT no SQL.
- **Teste de Expiração:** Definir um TTL curto (ex: 10s) e validar se a chave desaparece do RedisInsight após o tempo.
- **Teste de Estoque:** Tentar adicionar ao carrinho uma quantidade maior do que a presente na tabela SQL de produtos.
- **Teste de Ranking:** Realizar consultas em 3 produtos diferentes em volumes distintos e verificar se a opção de menu "Ranking" os exibe na ordem correta de popularidade.

