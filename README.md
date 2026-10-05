# Análise de E-commerce

Projeto de análise de dados de um e-commerce utilizando Python, SQL e Power BI. O objetivo foi analisar vendas, produtos, conversão e canais de aquisição, buscando identificar padrões e oportunidades de melhoria para o negócio.

## Ferramentas

* Python (Pandas)
* SQL / MySQL
* Power BI

## Principais indicadores

| Indicador         |        Resultado |
| ----------------- | ---------------: |
| Receita           | US$ 1.938.509,75 |
| Pedidos           |           32.313 |
| Ticket médio      |        US$ 59,99 |
| Lucro bruto       | US$ 1.216.139,50 |
| Margem bruta      |           62,74% |
| Taxa de conversão |            6,83% |

## Principais insights

* O **Mr Fuzzy** representa aproximadamente 73% da receita, mostrando uma forte concentração das vendas em um único produto.
* A conversão no **desktop foi de 8,50%**, contra **3,09% no mobile**, indicando uma oportunidade de investigar a experiência de compra em dispositivos móveis.
* Clientes recorrentes apresentaram conversão de **7,83%**, acima dos **6,64%** dos novos clientes.
* As campanhas apresentaram diferenças relevantes de desempenho. A campanha `brand` teve conversão de **7,79%**, enquanto `pilot` ficou em **1,08%**.
* O desempenho das diferentes fontes de tráfego também apresentou variações relevantes na taxa de conversão, permitindo comparar a eficiência dos canais de aquisição.

## Dashboard

O dashboard desenvolvido no Power BI apresenta indicadores de pedidos, ticket médio, receita, evolução das vendas, desempenho dos produtos e conversão por dispositivo e canais de aquisição.

O arquivo está disponível na pasta `PowerBI`.

## Estrutura

```text
Data/raw       → Dados originais
Notebooks      → Análise em Python
PowerBI        → Dashboard
SQL            → Consultas SQL
```

## Período analisado

Março de 2012 a março de 2015.
