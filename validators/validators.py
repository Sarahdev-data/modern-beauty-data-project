import numpy as np
import pandas as pd
import logging
from typing import Type, List
from pydantic import BaseModel, ValidationError
from schemas.schemas import VendaSchemas, ProdutoSchemas, CustoSchemas, ClienteSchemas, CampanhaSchemas

"""
    Valida cada linha de um DataFrame usando um schema Pydantic.
    Retorna apenas as linhas válidas.
"""

def validate_dataframe(df: pd.DataFrame, schema: Type[BaseModel]) -> pd.DataFrame:
    # Converte NaN para None para o Pydantic aceitar o Optional
    # Isso evita que o Pydantic se perca com o tipo float(nan)
    df_to_validate = df.replace({np.nan: None, pd.NA: None, pd.NaT: None})

    valid_rows: List[dict] = []
    error_rows: List[dict] = []

    for index, row in df_to_validate.iterrows():
        try:
            # O Pydantic valida o None e, se for Optional, deixa passar
            validated = schema(**row.to_dict())
            valid_rows.append(validated.model_dump())
        except ValidationError as e:
            error_rows.append({
                "row_index":index,
                "error":str(e),
                "data":row.to_dict()
            })
    
    return pd.DataFrame(valid_rows), pd.DataFrame(error_rows)


def validate_vendas(df: pd.DataFrame) -> pd.DataFrame:
    return validate_dataframe(df, VendaSchemas)

def validate_produtos(df: pd.DataFrame)-> pd.DataFrame:
    return validate_dataframe(df, ProdutoSchemas)

def validate_custos(df: pd.DataFrame) -> pd.DataFrame:
    return validate_dataframe(df, CustoSchemas)

def validate_clientes(df: pd.DataFrame) -> pd.DataFrame:
    return validate_dataframe(df, ClienteSchemas)

def validate_campanhas(df: pd.DataFrame) -> pd.DataFrame:
    return validate_dataframe(df, CampanhaSchemas)