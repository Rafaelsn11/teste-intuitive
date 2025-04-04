COPY operadoras(
    reg_ans, cnpj, razao_social, nome_fantasia, modalidade,
    logradouro, numero, complemento, bairro, cidade, uf, cep,
    ddd, telefone, fax, email, representante, cargo_representante,
    regiao_comercializacao, data_registro
)
FROM './datas/Relatorio_cadop.csv' 
WITH (
    FORMAT CSV, 
    HEADER true, 
    DELIMITER ';', 
    ENCODING 'UTF8',
    NULL ''
);

COPY quarterly_data(
    reg_ans,
    cd_conta_contabil,
    descricao,
    vl_saldo_inicial,
    vl_saldo_final,
    data_referencia
)
FROM './datas/1T2021.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);

COPY quarterly_data(
    reg_ans,
    cd_conta_contabil,
    descricao,
    vl_saldo_inicial,
    vl_saldo_final,
    data_referencia
)
FROM './datas/2T2021.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);

COPY quarterly_data(
    reg_ans,
    cd_conta_contabil,
    descricao,
    vl_saldo_inicial,
    vl_saldo_final,
    data_referencia
)
FROM './datas/3T2021.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);

COPY quarterly_data(
    reg_ans,
    cd_conta_contabil,
    descricao,
    vl_saldo_inicial,
    vl_saldo_final,
    data_referencia
)
FROM './datas/4T2021.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);