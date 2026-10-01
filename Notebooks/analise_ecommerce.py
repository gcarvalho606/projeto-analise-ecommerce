from mimetypes import init

import pandas as pd


# Carregar as tabelas

orders = pd.read_csv("Data/raw/orders.csv")
order_items = pd.read_csv("Data/raw/order_items.csv")
order_item_refunds = pd.read_csv("Data/raw/order_item_refunds.csv")
products = pd.read_csv("Data/raw/products.csv")
website_sessions = pd.read_csv("Data/raw/website_sessions.csv")
website_pageviews = pd.read_csv("Data/raw/website_pageviews.csv")


# Verificar quantidade de linhas e colunas

print("ORDERS")
print("Linhas:", len(orders))
print("Colunas:", len(orders.columns))

print("\nORDER ITEMS")
print("Linhas:", len(order_items))
print("Colunas:", len(order_items.columns))

print("\nORDER ITEM REFUNDS")
print("Linhas:", len(order_item_refunds))
print("Colunas:", len(order_item_refunds.columns))

print("\nPRODUCTS")
print("Linhas:", len(products))
print("Colunas:", len(products.columns))

print("\nWEBSITE SESSIONS")
print("Linhas:", len(website_sessions))
print("Colunas:", len(website_sessions.columns))

print("\nWEBSITE PAGEVIEWS")
print("Linhas:", len(website_pageviews))
print("Colunas:", len(website_pageviews.columns))


print("Receita total:", orders["price_usd"].sum())
print("Custo total:", orders["cogs_usd"].sum())


# Converter colunas de data para datetime

orders["created_at"] = pd.to_datetime(orders["created_at"])
order_items["created_at"] = pd.to_datetime(order_items["created_at"])
order_item_refunds["created_at"] = pd.to_datetime(order_item_refunds["created_at"])
products["created_at"] = pd.to_datetime(products["created_at"])
website_sessions["created_at"] = pd.to_datetime(website_sessions["created_at"])
website_pageviews["created_at"] = pd.to_datetime(website_pageviews["created_at"])


# Período dos dados

print("\nPERÍODO DOS DADOS")
print("Primeiro pedido:", orders["created_at"].min())
print("Último pedido:", orders["created_at"].max())


# Resumo financeiro

receita = orders["price_usd"].sum()
custo = orders["cogs_usd"].sum()
lucro_bruto = receita - custo
margem_bruta = lucro_bruto / receita * 100

print("\nRESUMO FINANCEIRO")
print("Receita total: US$", round(receita, 2))
print("Custo total: US$", round(custo, 2))
print("Lucro bruto: US$", round(lucro_bruto, 2))
print("Margem bruta:", round(margem_bruta, 2), "%")


# Resumo de pedidos

total_pedidos = orders["order_id"].nunique()
ticket_medio = orders["price_usd"].sum() / total_pedidos

print("\nRESUMO DE PEDIDOS")
print("Total de pedidos:", total_pedidos)
print("Ticket médio: US$", round(ticket_medio, 2))


# Vendas por mês

vendas_mensais = (
    orders
    .set_index("created_at")
    .resample("ME")["price_usd"]
    .sum()
)

print("\nVENDAS POR MÊS")
print(vendas_mensais)


# Pedidos por mês

pedidos_mensais = (
    orders
    .set_index("created_at")
    .resample("ME")["order_id"]
    .count()
)

print("\nPEDIDOS POR MÊS")
print(pedidos_mensais)


# Ticket médio por mês

ticket_medio_mensal = (
    orders
    .set_index("created_at")
    .resample("ME")
    .agg(
        receita=("price_usd", "sum"),
        pedidos=("order_id", "count")
    )
)

ticket_medio_mensal["ticket_medio"] = (
    ticket_medio_mensal["receita"]
    / ticket_medio_mensal["pedidos"]
)

print("\nTICKET MÉDIO POR MÊS")
print(ticket_medio_mensal)

# Vendas por produto com nome

vendas_produto = (
    orders
    .merge(
        products,
        left_on="primary_product_id",
        right_on="product_id",
        how="left"
    )
    .groupby(["primary_product_id", "product_name"])
    .agg(
        pedidos=("order_id", "count"),
        receita=("price_usd", "sum"),
        custo=("cogs_usd", "sum")
    )
)

vendas_produto["lucro_bruto"] = (
    vendas_produto["receita"] - vendas_produto["custo"]
)

vendas_produto["margem_bruta"] = (
    vendas_produto["lucro_bruto"]
    / vendas_produto["receita"]
    * 100
)

print("\nVENDAS POR PRODUTO")
print(vendas_produto)


# Quantidade de unidades vendidas por produto

unidades_produto = (
    order_items
    .groupby("product_id")
    .agg(
        unidades_vendidas=("order_item_id", "count")
    )
    .reset_index()
    .merge(
        products,
        on="product_id",
        how="left"
    )
    .sort_values("unidades_vendidas", ascending=False)
)

print("\nUNIDADES VENDIDAS POR PRODUTO")
print(unidades_produto)


# Data de lançamento dos produtos

print("\nPRODUTOS E DATA DE LANÇAMENTO")

print(
    products[
        ["product_id", "product_name", "created_at"]
    ].sort_values("created_at")
)


# Ranking de produtos por receita

ranking_produtos = (
    vendas_produto
    .reset_index()
    .sort_values("receita", ascending=False)
)

print("\nRANKING DE PRODUTOS POR RECEITA")

print(
    ranking_produtos[
        [
            "product_name",
            "pedidos",
            "receita",
            "lucro_bruto",
            "margem_bruta"
        ]
    ]
)


# Participação de cada produto na receita total

ranking_produtos["participacao_receita"] = (
    ranking_produtos["receita"]
    / ranking_produtos["receita"].sum()
    * 100
)

print("\nPARTICIPAÇÃO NA RECEITA")

print(
    ranking_produtos[
        [
            "product_name",
            "receita",
            "participacao_receita"
        ]
    ]
)


# Sessões novas vs. recorrentes

sessoes_tipo = (
    website_sessions["is_repeat_session"]
    .value_counts()
    .rename(
        index={
            0: "Novas",
            1: "Recorrentes"
        }
    )
)

print("\nSESSÕES NOVAS VS. RECORRENTES")
print(sessoes_tipo)


# Conversão de sessões em pedidos

total_sessoes = website_sessions["website_session_id"].nunique()
sessoes_com_pedido = orders["website_session_id"].nunique()

taxa_conversao = sessoes_com_pedido / total_sessoes * 100

print("\nCONVERSÃO DE SESSÕES EM PEDIDOS")
print("Total de sessões:", total_sessoes)
print("Sessões com pedido:", sessoes_com_pedido)
print("Taxa de conversão:", round(taxa_conversao, 2), "%")


# Conversão por tipo de sessão

sessoes_com_pedido_tipo = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

sessoes_com_pedido_tipo["converteu"] = (
    sessoes_com_pedido_tipo["_merge"] == "both"
)

conversao_tipo = (
    sessoes_com_pedido_tipo
    .groupby("is_repeat_session")
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

conversao_tipo["taxa_conversao"] = (
    conversao_tipo["sessoes_com_pedido"]
    / conversao_tipo["sessoes"]
    * 100
)

conversao_tipo.index = conversao_tipo.index.map(
    {
        0: "Novas",
        1: "Recorrentes"
    }
)

print("\nCONVERSÃO POR TIPO DE SESSÃO")
print(conversao_tipo)


# Sessões e conversão por dispositivo

sessoes_dispositivo = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

sessoes_dispositivo["converteu"] = (
    sessoes_dispositivo["_merge"] == "both"
)

conversao_dispositivo = (
    sessoes_dispositivo
    .groupby("device_type")
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

conversao_dispositivo["taxa_conversao"] = (
    conversao_dispositivo["sessoes_com_pedido"]
    / conversao_dispositivo["sessoes"]
    * 100
)

print("\nCONVERSÃO POR DISPOSITIVO")
print(
    conversao_dispositivo.sort_values(
        "taxa_conversao",
        ascending=False
    )
)


# Sessões e conversão por origem do tráfego

trafego = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

trafego["converteu"] = (
    trafego["_merge"] == "both"
)

conversao_fonte = (
    trafego
    .groupby("utm_source", dropna=False)
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

conversao_fonte["taxa_conversao"] = (
    conversao_fonte["sessoes_com_pedido"]
    / conversao_fonte["sessoes"]
    * 100
)

print("\nCONVERSÃO POR ORIGEM DO TRÁFEGO")

print(
    conversao_fonte
    .sort_values("sessoes", ascending=False)
)


# Conversão por campanha

campanhas = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

campanhas["converteu"] = (
    campanhas["_merge"] == "both"
)

conversao_campanha = (
    campanhas
    .groupby("utm_campaign", dropna=False)
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

conversao_campanha["taxa_conversao"] = (
    conversao_campanha["sessoes_com_pedido"]
    / conversao_campanha["sessoes"]
    * 100
)

print("\nCONVERSÃO POR CAMPANHA")

print(
    conversao_campanha
    .sort_values("sessoes", ascending=False)
)


# Conversão por origem e campanha

origem_campanha = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

origem_campanha["converteu"] = (
    origem_campanha["_merge"] == "both"
)

resultado_origem_campanha = (
    origem_campanha
    .groupby(
        ["utm_source", "utm_campaign"],
        dropna=False
    )
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

resultado_origem_campanha["taxa_conversao"] = (
    resultado_origem_campanha["sessoes_com_pedido"]
    / resultado_origem_campanha["sessoes"]
    * 100
)

print("\nCONVERSÃO POR ORIGEM E CAMPANHA")
print(resultado_origem_campanha)


# Conversão por conteúdo

conteudo = (
    website_sessions
    .merge(
        orders[["website_session_id"]].drop_duplicates(),
        on="website_session_id",
        how="left",
        indicator=True
    )
)

conteudo["converteu"] = (
    conteudo["_merge"] == "both"
)

resultado_conteudo = (
    conteudo
    .groupby("utm_content", dropna=False)
    .agg(
        sessoes=("website_session_id", "count"),
        sessoes_com_pedido=("converteu", "sum")
    )
)

resultado_conteudo["taxa_conversao"] = (
    resultado_conteudo["sessoes_com_pedido"]
    / resultado_conteudo["sessoes"]
    * 100
)

print("\nCONVERSÃO POR CONTEÚDO")

print(
    resultado_conteudo
    .sort_values("sessoes", ascending=False)
)


# Resumo de reembolsos

total_reembolsos = order_item_refunds[
    "order_item_refund_id"
].nunique()

valor_reembolsado = order_item_refunds[
    "refund_amount_usd"
].sum()

print("\nRESUMO DE REEMBOLSOS")
print("Total de reembolsos:", total_reembolsos)
print(
    "Valor total reembolsado: US$",
    round(valor_reembolsado, 2)
)


# Impacto dos reembolsos na receita

receita_total = orders["price_usd"].sum()

percentual_reembolsado = (
    valor_reembolsado / receita_total * 100
)

print("\nIMPACTO DOS REEMBOLSOS")
print("Receita bruta: US$", round(receita_total, 2))
print(
    "Valor reembolsado: US$",
    round(valor_reembolsado, 2)
)
print(
    "Percentual da receita reembolsado:",
    round(percentual_reembolsado, 2),
    "%"
)


# Reembolsos por produto

reembolsos_produto = (
    order_item_refunds
    .merge(
        order_items[["order_item_id", "product_id"]],
        on="order_item_id",
        how="left"
    )
    .merge(
        products[["product_id", "product_name"]],
        on="product_id",
        how="left"
    )
    .groupby(
        ["product_id", "product_name"]
    )
    .agg(
        quantidade_reembolsos=(
            "order_item_refund_id",
            "count"
        ),
        valor_reembolsado=(
            "refund_amount_usd",
            "sum"
        )
    )
    .sort_values(
        "valor_reembolsado",
        ascending=False
    )
)

print("\nREEMBOLSOS POR PRODUTO")
print(reembolsos_produto)

