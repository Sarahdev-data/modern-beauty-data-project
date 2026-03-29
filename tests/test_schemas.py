import pandas as pd
import pytest
from typing import List, Dict, Any
from validators.validators import validate_vendas, validate_produtos, validate_custos, validate_clientes, validate_campanhas

""" Testando Validação de Tipos em Vendas """
@pytest.mark.parametrize("dados, esperado_validos, descricao",[
    # Cenário 1: Tipos corretos (int, str, datetime string)
    ([{"id_venda": "V00001", "data_venda": "2025-11-01", "id_cliente": "C0001", "id_produto": "P0021", "quantidade": 5, "forma_pagamento": "PIX"}], 1, "Dados válidos"),
    # Cenário 2: Quantidade está em formato de string, porém deveria ser int
    ([{"id_venda": "V00001", "data_venda": "2025-11-01", "id_cliente": "C0001", "id_produto": "P0021", "quantidade": "cinco", "forma_pagamento": "PIX"}], 0, "Quantidade inválida"),
    # Cenário 3: Formato de data inválido
    ([{"id_venda": "V00001", "data_venda": "um do onze", "id_cliente": "C0001", "id_produto": "P0021", "quantidade": 5, "forma_pagamento": "PIX"}], 0, "Data inválida"),
])

def test_validate_vendas(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    
    # Receba o DF de sucessos e o de erros
    df_validado, df_erros = validate_vendas(df) 
    
    # O assert continua validando se a quantidade de linhas válidas é a esperada
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    
    # Valida se o erro realmente foi gerado quando esperado
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"


""" Testando Validação de Tipos em Produtos """
@pytest.mark.parametrize("dados, esperado_validos, descricao",[
    # Cenário 1: Tudo correto (Tipos: str, float, str)
    ([{"id_produto": "P0001", "nome_produto": "Cereja e Avelã", "categoria": "Body Splash", "marca": "Natura", "volume_ml": 200.0, "preco_unitario": 74.90, "ativo": "Sim"}], 1, "Sucesso total"),
    # Cenário 2: Preço Unitário com o tipo errado (String em vez de float)
    ([{"id_produto": "P0001", "nome_produto": "Cereja e Avelã", "categoria": "Body Splash", "marca": "Natura", "volume_ml": 200.0, "preco_unitario": "setenta e quatro", "ativo": "Sim"}], 0, "Erro, preço unitário não é número!"),
    # Cenário 3: Preço Unitário com VALOR errado (Regra Field(gt=0))
    ([{"id_produto": "P0001", "nome_produto": "Cereja e Avelã", "categoria": "Body Splash", "marca": "Natura", "volume_ml": 200.0, "preco_unitario": -74.90, "ativo": "Sim"}], 0, "Erro: preco_unitario <= 0"),
    # Cenário 4: Volume ML com TIPO errado (String em vez de float)
    ([{"id_produto": "P0001", "nome_produto": "Cereja e Avelã", "categoria": "Body Splash", "marca": "Natura", "volume_ml": "duzentos ml", "preco_unitario": 74.90, "ativo": "Sim"}], 0, "Volume com tipo errado")
])

def test_validate_produtos(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    df_validado, df_erros = validate_produtos(df)
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"


""" Testando Validação de Tipos de Custos """
@pytest.mark.parametrize("dados, esperado_validos, descricao", [
    # Cenário 1: Tudo correto
    ([{"id_produto":"P0005", "custo_unitario": 117.80, "fornecedor": "Eudora"}], 1, "Informações corretas"),
    # Cenário 2: Custo Unitário menor que zero
    ([{"id_produto":"P0005", "custo_unitario": -117.80, "fornecedor": "Eudora"}], 0, "Valor do custo unitário incorreto")
])

def test_validate_custos(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    df_validado, df_erros = validate_custos(df)
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"


""" Testando Validação de Tipos em Clientes """
@pytest.mark.parametrize("dados, esperado_validos, descricao", [
    # Cenário 1: Tudo correto, todos os campos preenchidos
    ([{"id_cliente": "C0001", "nome_cliente": "João", "email": "j@test.com", "sexo": "Masculino", "data_nascimento": "1990-11-01", "cidade": "São Paulo", "estado": "SP", "data_cadastro": "2023-01-01", "fonte_aquisicao": "Indicação"}], 1, "Informações completas"),
    # Cenário 2: Campo obrigatório (email) faltando/nulo
    ([{"id_cliente": "C0001", "nome_cliente": "João", "email": None, "sexo": "Masculino", "data_nascimento": "1990-11-01", "cidade": "São Paulo", "estado": "SP", "data_cadastro": "2023-01-01", "fonte_aquisicao": "Indicação"}], 0, "Informações incompletas")
])

def test_validate_clientes(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    df_validado, df_erros = validate_clientes(df)
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"


""" Testando Validação de Tipos em Campanhas """
@pytest.mark.parametrize("dados, esperado_validos, descricao", [
    # Cenário 1: Tudo correto
    ([{"id_campanha": "MKT003", "canal": "Marketplace", "data_inicio": "2025-11-01", "data_fim": "2025-11-30", "investimento": 12000, "ref": "Black Friday"}], 1, "Informações corretas"),
    # Cenário 2: Data início e data fim com formatos incorretos (string)
    ([{"id_campanha": "MKT003", "canal": "Marketplace", "data_inicio": "um do onze", "data_fim": "trinta do onze", "investimento": 12000, "ref": "Black Friday"}], 0, "Data início e data fim com tipos incorretos"),
    # Cenário 3: Investimento como string
    ([{"id_campanha": "MKT003", "canal": "Marketplace", "data_inicio": "2025-11-01", "data_fim": "2025-11-30", "investimento": "doze mil", "ref": "Black Friday"}], 0, "Coluna investimento com tipo errado")
])

def test_validate_campanhas(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    df_validado, df_erros = validate_campanhas(df)
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"


""" Testando valores nulos """
@pytest.mark.parametrize("dados, esperado_validos, descricao", [
    # volume_ml é Optional: deve aceitar 1 linha
    ([{"id_produto": "P0001", "nome_produto": "Kit", "categoria": "K", "marca": "N", "volume_ml": None, "preco_unitario": 100.0, "ativo": "Sim"}], 1, "Volume nulo permitido"),
    
    # preco_unitario NÃO é Optional: deve retornar 0 linhas válidas
    ([{"id_produto": "P0001", "nome_produto": "Kit", "categoria": "K", "marca": "N", "volume_ml": 100.0, "preco_unitario": None, "ativo": "Sim"}], 0, "Preço nulo rejeitado"),
])

def test_produtos_opcionais(dados: List[Dict[str, Any]], esperado_validos: int, descricao: str) -> None:
    df: pd.DataFrame = pd.DataFrame(dados)
    df_validado, df_erros = validate_produtos(df)
    assert len(df_validado) == esperado_validos, f"Falhou em: {descricao}"
    if esperado_validos == 0:
        assert len(df_erros) > 0, f"Deveria ter retornado erro para: {descricao}"
