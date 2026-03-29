import pandas as pd

def métricas_vendas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["receita"] = (df["quantidade"] * df["preco_unitario"]).round(2)
    df["custo_total"] = (df["quantidade"] * df["custo_unitario"]).round(2)
    df["lucro"] = (df["receita"] - df["custo_total"]).round(2)
    df["margem_pct"] = ((df["lucro"] / df["receita"]) * 100).round(2)

    # Métricas auxiliares
    df["ticket_venda"] = df["receita"]
    df["ano_mes"] = df["data_venda"].dt.to_period("M").astype(str)

    return df