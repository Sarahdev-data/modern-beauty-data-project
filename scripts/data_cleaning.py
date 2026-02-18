import pandas as pd

def clean_vendas(df: pd.DataFrame):

    df = df.copy()

    id = {
        'P001':'P0001',
        'P002':'P0002',
        'P003':'P0003',
        'P004':'P0004',
        'P005':'P0005',
        'P006':'P0006',
        'P007':'P0007',
        'P008':'P0008',
        'P009':'P0009'
    }
    df["id_produto"] = df["id_produto"].replace(id)
    df["id_produto"] = df["id_produto"].str.strip()

    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    df = df.dropna(subset=["data_venda"])

    df["forma_pagamento"] = df["forma_pagamento"].str.strip().str.upper()

    return df


def clean_produtos(df: pd.DataFrame):
    df = df.copy()

    df["id_produto"] = df["id_produto"].str.strip()

    df["nome_produto"] = df["nome_produto"].str.strip()
    df["nome_produto"] = df["nome_produto"].str.title()

    df["categoria"] = df["categoria"].str.strip().str.title()
    
    marca = {
        'Natura Fotoequilíbrio': 'Natura',
        'Natura Chronos': 'Natura',
    }
    df["marca"] = df["marca"].replace(marca)
    df["marca"] = df["marca"].str.strip().str.title()

    df["volume_ml"] = pd.to_numeric(df["volume_ml"], errors="coerce")

    return df


def clean_custos(df:pd.DataFrame):
    df = df.copy()

    fornecedor = {
        'Natura Fotoequilíbrio': 'Natura',
        'Natura Chronos': 'Natura',
    }

    df["fornecedor"] = df["fornecedor"].str.strip().replace(fornecedor)
    df["fornecedor"] = df["fornecedor"].str.title()
    return df


def clean_clientes_atualizado(df:pd.DataFrame):
    df = df.copy()

    df["nome_cliente"] = df["nome_cliente"].str.strip().str.title()

    df["email"] = df["email"].str.strip()

    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce")
    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], errors="coerce")

    genero = {
        'F':'Feminino',
        'M':'Masculino'
    }
    df["sexo"] = df["sexo"].str.strip().replace(genero)

    df["fonte_aquisicao"] = df["fonte_aquisicao"].str.title()

    cidade = {
        'Uberlandia':'Uberlândia',
        'Campina':'Campinas',
        'POA':'Porto Alegre',
        'Rio':'Rio de Janeiro',
        'Niteroi':'Niterói'
    }
    df["cidade"] = df["cidade"].str.strip().replace(cidade)

    return df


def clean_campanhas_marketing(df:pd.DataFrame):
    df = df.copy()

    df["canal"] = df["canal"].str.strip()

    df["data_inicio"] = pd.to_datetime(df["data_inicio"], errors="coerce")
    df["data_fim"] = pd.to_datetime(df["data_fim"], errors="coerce")

    df["ref"] = df["ref"].str.strip()
    
    return df