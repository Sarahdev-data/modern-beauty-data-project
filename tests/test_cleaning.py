import pytest
import pandas as pd
from typing import Any, Dict
from scripts.data_cleaning import clean_vendas, clean_produtos, clean_custos, clean_clientes_atualizado, clean_campanhas_marketing

def test_clean_vendas() -> None :
    data: Dict[str, Any] = {
        "id_produto":["P005"],
        "data_venda": ["2025-01-12"],
        "forma_pagamento":[" pix "]
    }
    df_input = pd.DataFrame(data)

    df_result: pd.DataFrame = clean_vendas(df_input)

    assert df_result.loc[0, "id_produto"] == "P0005"
    assert df_result.loc[0, "forma_pagamento"] == "PIX"


def test_clean_produtos() -> None :
    data: Dict[str, Any] = {
        "id_produto": ["P0005 ", " P0015"],
        "nome_produto": ["Essencial Exclusivo ", "essencial exclusivo"],
        "categoria": ["Perfume ","perfume"],
        "marca": ["Natura Chronos", "natura chronos"],
        "volume_ml": ["500", "20"]
    }
    df_input = pd.DataFrame(data)

    df_result: pd.DataFrame = clean_produtos(df_input)

    assert df_result.loc[1, "id_produto"] == "P0015"
    assert df_result.loc[1, "nome_produto"] == "Essencial Exclusivo"
    assert df_result.loc[1, "categoria"] == "Perfume"
    assert df_result.loc[1, "marca"] == "Natura"
    assert df_result.loc[1, "volume_ml"] == 20.0


def test_clean_custos() -> None :
    data: Dict[str, Any] = {
        "fornecedor": ["Natura Fotoequilíbrio", "natura fotoequilíbrio", "Natura "]
    }
    df_input = pd.DataFrame(data)

    df_result: pd.DataFrame = clean_custos(df_input)

    assert df_result.loc[0, "fornecedor"] == "Natura"
    assert df_result.loc[1, "fornecedor"] == "Natura"
    assert df_result.loc[2, "fornecedor"] == "Natura"


def test_clean_clientes_atualizado() -> None :
    data: Dict[str, Any] = {
        "nome_cliente": ["Ana ", "ana"],
        "email": [" ana@email.com ", "ana@email.com "],
        "data_nascimento": ["1990-03-15", "22/05/1995"],
        "data_cadastro": ["2023-08-22", "2024-10-11"],
        "sexo": ["F", "Feminino "],
        "fonte_aquisicao": ["E-mail marketing", "e-mail marketing"],
        "cidade": ["POA", "Rio de Janeiro "]
    }
    df_input = pd.DataFrame(data)

    df_result: pd.DataFrame = clean_clientes_atualizado(df_input)

    assert df_result.loc[0, "nome_cliente"] == "Ana"
    assert df_result.loc[0, "email"] == "ana@email.com"
    assert df_result.loc[0, "data_nascimento"].year == 1990
    assert df_result.loc[0, "data_nascimento"].month == 3
    assert df_result.loc[0, "data_cadastro"].month == 8
    assert df_result.loc[0, "sexo"] == "Feminino"
    assert df_result.loc[0, "fonte_aquisicao"] == "E-Mail Marketing"
    assert df_result.loc[0, "cidade"] == "Porto Alegre"


def test_clean_campanhas_marketing() -> None :
    data: Dict[str, Any] = {
        "canal": ["Google Ads "],
        "data_inicio": ["2025-10-15"],
        "data_fim": ["2025-10-31"],
        "ref": [" Black Friday "]
    }
    df_input = pd.DataFrame(data)

    df_result: pd.DataFrame = clean_campanhas_marketing(df_input)

    assert df_result.loc[0, "canal"] == "Google Ads"
    assert df_result.loc[0, "data_inicio"].year == 2025
    assert df_result.loc[0, "data_inicio"].month == 10
    assert df_result.loc[0, "data_fim"].year == 2025
    assert df_result.loc[0, "data_fim"].month == 10
    assert df_result.loc[0, "ref"] == "Black Friday"