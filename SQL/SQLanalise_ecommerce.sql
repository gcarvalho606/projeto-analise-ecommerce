USE ecommerce_analytics;


-- ============================================================
-- 1. VISÃO GERAL DO NEGÓCIO
-- ============================================================

SELECT
    SUM(price_usd) AS receita_total,
    SUM(cogs_usd) AS custo_total,
    SUM(price_usd) - SUM(cogs_usd) AS lucro_bruto,
    ROUND(
        (SUM(price_usd) - SUM(cogs_usd))
        / SUM(price_usd) * 100,
        2
    ) AS margem_bruta
FROM orders;


-- ============================================================
-- 2. TOTAL DE PEDIDOS E TICKET MÉDIO
-- ============================================================

SELECT
    COUNT(*) AS total_pedidos,
    ROUND(SUM(price_usd) / COUNT(*), 2) AS ticket_medio
FROM orders;


-- ============================================================
-- 3. RECEITA E LUCRO POR PRODUTO
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    COUNT(DISTINCT oi.order_id) AS total_pedidos,
    ROUND(SUM(oi.price_usd), 2) AS receita,
    ROUND(SUM(oi.cogs_usd), 2) AS custo,
    ROUND(SUM(oi.price_usd) - SUM(oi.cogs_usd), 2) AS lucro,
    ROUND(
        (SUM(oi.price_usd) - SUM(oi.cogs_usd))
        / SUM(oi.price_usd) * 100,
        2
    ) AS margem_bruta
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY receita DESC;


-- ============================================================
-- 4. PEDIDOS, RECEITA E LUCRO POR MÊS
-- ============================================================

SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS mes,
    COUNT(*) AS total_pedidos,
    ROUND(SUM(price_usd), 2) AS receita,
    ROUND(SUM(cogs_usd), 2) AS custo,
    ROUND(SUM(price_usd) - SUM(cogs_usd), 2) AS lucro
FROM orders
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY mes;


-- ============================================================
-- 5. CONVERSÃO GERAL DO SITE
-- ============================================================

SELECT
    COUNT(DISTINCT ws.website_session_id) AS total_sessoes,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / COUNT(DISTINCT ws.website_session_id) * 100,
        2
    ) AS taxa_conversao
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id;


-- ============================================================
-- 6. CONVERSÃO POR TIPO DE USUÁRIO
-- ============================================================

SELECT
    CASE
        WHEN ws.is_repeat_session = 1 THEN 'Returning'
        ELSE 'New'
    END AS tipo_usuario,
    COUNT(DISTINCT ws.website_session_id) AS sessoes,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / COUNT(DISTINCT ws.website_session_id) * 100,
        2
    ) AS taxa_conversao
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id
GROUP BY
    CASE
        WHEN ws.is_repeat_session = 1 THEN 'Returning'
        ELSE 'New'
    END
ORDER BY taxa_conversao DESC;


-- ============================================================
-- 7. CONVERSÃO POR DISPOSITIVO
-- ============================================================

SELECT
    COALESCE(ws.device_type, 'Unknown') AS dispositivo,
    COUNT(DISTINCT ws.website_session_id) AS sessoes,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / COUNT(DISTINCT ws.website_session_id) * 100,
        2
    ) AS taxa_conversao
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id
GROUP BY
    COALESCE(ws.device_type, 'Unknown')
ORDER BY taxa_conversao DESC;


-- ============================================================
-- 8. CONVERSÃO POR ORIGEM DE TRÁFEGO
-- ============================================================

SELECT
    COALESCE(ws.utm_source, 'Direct') AS origem,
    COUNT(DISTINCT ws.website_session_id) AS sessoes,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / COUNT(DISTINCT ws.website_session_id) * 100,
        2
    ) AS taxa_conversao
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id
GROUP BY
    COALESCE(ws.utm_source, 'Direct')
ORDER BY taxa_conversao DESC;


-- ============================================================
-- 9. CONVERSÃO POR CAMPANHA
-- ============================================================

SELECT
    COALESCE(ws.utm_campaign, 'No Campaign') AS campanha,
    COUNT(DISTINCT ws.website_session_id) AS sessoes,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / COUNT(DISTINCT ws.website_session_id) * 100,
        2
    ) AS taxa_conversao
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id
GROUP BY
    COALESCE(ws.utm_campaign, 'No Campaign')
ORDER BY taxa_conversao DESC;


-- ============================================================
-- 10. RECEITA POR ORIGEM DE TRÁFEGO
-- ============================================================

SELECT
    COALESCE(ws.utm_source, 'Direct') AS origem,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(SUM(o.price_usd), 2) AS receita,
    ROUND(
        SUM(o.price_usd) / COUNT(DISTINCT o.order_id),
        2
    ) AS ticket_medio
FROM orders o
JOIN website_sessions ws
    ON o.website_session_id = ws.website_session_id
GROUP BY
    COALESCE(ws.utm_source, 'Direct')
ORDER BY receita DESC;


-- ============================================================
-- 11. PERFORMANCE POR CAMPANHA
-- ============================================================

SELECT
    COALESCE(ws.utm_campaign, 'No Campaign') AS campanha,
    COUNT(DISTINCT o.order_id) AS pedidos,
    ROUND(SUM(o.price_usd), 2) AS receita,
    ROUND(SUM(o.cogs_usd), 2) AS custo,
    ROUND(SUM(o.price_usd) - SUM(o.cogs_usd), 2) AS lucro
FROM orders o
JOIN website_sessions ws
    ON o.website_session_id = ws.website_session_id
GROUP BY
    COALESCE(ws.utm_campaign, 'No Campaign')
ORDER BY receita DESC;


-- ============================================================
-- 12. PÁGINAS MAIS ACESSADAS
-- ============================================================

SELECT
    pageview_url,
    COUNT(*) AS total_visualizacoes
FROM website_pageviews
GROUP BY pageview_url
ORDER BY total_visualizacoes DESC;


-- ============================================================
-- 13. PAGEVIEWS POR MÊS
-- ============================================================

SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS mes,
    COUNT(*) AS total_pageviews
FROM website_pageviews
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY mes;


-- ============================================================
-- 14. PEDIDOS POR PRODUTO PRINCIPAL
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    COUNT(*) AS total_pedidos,
    ROUND(SUM(o.price_usd), 2) AS receita,
    ROUND(SUM(o.cogs_usd), 2) AS custo,
    ROUND(SUM(o.price_usd) - SUM(o.cogs_usd), 2) AS lucro
FROM orders o
JOIN products p
    ON o.primary_product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY receita DESC;


-- ============================================================
-- 15. QUANTIDADE MÉDIA DE ITENS POR PEDIDO
-- ============================================================

SELECT
    ROUND(AVG(items_purchased), 2) AS media_itens_por_pedido
FROM orders;


-- ============================================================
-- 16. PEDIDOS POR QUANTIDADE DE ITENS
-- ============================================================

SELECT
    items_purchased,
    COUNT(*) AS total_pedidos,
    ROUND(SUM(price_usd), 2) AS receita
FROM orders
GROUP BY items_purchased
ORDER BY items_purchased;


-- ============================================================
-- 17. EVOLUÇÃO MENSAL DE PEDIDOS E TICKET MÉDIO
-- ============================================================

SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS mes,
    COUNT(*) AS pedidos,
    ROUND(SUM(price_usd) / COUNT(*), 2) AS ticket_medio
FROM orders
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY mes;
