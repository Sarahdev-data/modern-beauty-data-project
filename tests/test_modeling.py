import pytest
import pandas as pd
from typing import Dict, Any
from scripts.data_modeling import métricas_vendas

def test_metricas_vendas() -> None:
    data: Dict[str, Any] = {
        "quantidade":[2,10],
        "preco_unitario":[50.0,10.0],
        "custo_unitario":[30.0,5.0],
        "data_venda": pd.to_datetime(["2025-01-15","2025-02-20"])
    }
    df_input: pd.DataFrame = pd.DataFrame(data)

    df_result: pd.DataFrame = métricas_vendas(df_input)

    # Testando a primeira linha:
    # Receita: 2 * 50 = 100 | Custo: 2 * 30 = 60 | Lucro: 40 | Margem: 40%
    assert df_result.loc[0, "receita"] == 100.0
    assert df_result.loc[0, "lucro"] == 40.0
    assert df_result.loc[0, "margem_pct"] == 40.0

    # Testando a formatação da data (ano_mes)
    assert df_result.loc[0, "ano_mes"] == "2025-01"
    assert df_result.loc[1, "ano_mes"] == "2025-02"

    # Testando se o ticket_venda é igual à receita
    assert df_result.loc[1, "ticket_venda"] == df_result.loc[1, "receita"]