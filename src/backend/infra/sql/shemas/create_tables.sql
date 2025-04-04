CREATE TABLE IF NOT EXISTS operadoras (
    reg_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(14),
    razao_social TEXT,
    nome_fantasia TEXT,
    modalidade TEXT,
    logradouro TEXT,
    numero VARCHAR(10),
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf VARCHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email TEXT,
    representante TEXT,
    cargo_representante TEXT,
    regiao_comercializacao INTEGER,
    data_registro DATE
);

CREATE TABLE IF NOT EXISTS quarterly_data (
    reg_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(20), 
    descricao TEXT,
    data_referencia DATE,
    vl_saldo_inicial NUMERIC(15,2),
    vl_saldo_final NUMERIC(15,2)
);

CREATE INDEX idx_quarterly_data_reg_ans ON quarterly_data(reg_ans);
CREATE INDEX idx_quarterly_data_conta ON quarterly_data(cd_conta_contabil);
CREATE INDEX idx_quarterly_data_data ON quarterly_data(data_referencia);