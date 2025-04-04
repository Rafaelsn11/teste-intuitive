-- Query 1: Top 10 operadoras com maiores despesas no último trimestre
WITH last_quarter AS (
    SELECT DATE_TRUNC('quarter', MAX(data_referencia)) as latest_quarter
    FROM quarterly_data
)
SELECT 
    o.razao_social,
    TO_CHAR(ABS(SUM(qd.vl_saldo_final)), 'FM999G999G999G999D99') as despesa_total,
    TO_CHAR(lq.latest_quarter, 'MM/YYYY') as periodo
FROM quarterly_data qd
JOIN operadoras o ON o.reg_ans = qd.reg_ans
JOIN last_quarter lq 
    ON DATE_TRUNC('quarter', qd.data_referencia) = lq.latest_quarter
WHERE qd.cd_conta_contabil LIKE '411%' 
    AND qd.descricao ILIKE '%EVENTOS/SINISTROS%ASSISTÊNCIA A SAÚDE%'
GROUP BY o.razao_social, lq.latest_quarter
ORDER BY SUM(qd.vl_saldo_final) DESC
LIMIT 10;

-- Query 2: Top 10 operadoras com maiores despesas no último ano
WITH last_year AS (
    SELECT EXTRACT(YEAR FROM MAX(data_referencia)) as year
    FROM quarterly_data
)
SELECT 
    o.razao_social,
    TO_CHAR(ABS(SUM(qd.vl_saldo_final)), 'FM999G999G999G999D99') as despesa_anual,
    ly.year as ano
FROM quarterly_data qd
JOIN operadoras o ON o.reg_ans = qd.reg_ans
JOIN last_year ly 
    ON EXTRACT(YEAR FROM qd.data_referencia) = ly.year
WHERE qd.cd_conta_contabil LIKE '411%' 
    AND qd.descricao ILIKE '%EVENTOS/SINISTROS%ASSISTÊNCIA A SAÚDE%'
GROUP BY o.razao_social, ly.year
ORDER BY SUM(qd.vl_saldo_final) DESC
LIMIT 10;