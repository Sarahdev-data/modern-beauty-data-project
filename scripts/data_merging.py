import pandas as pd

def vendas_e_produtos(vendas: pd.DataFrame, produtos: pd.DataFrame):

    vendas_produtos = vendas.merge(
        produtos,
        on="id_produto",          
        how="left"                                 
    )

    return vendas_produtos

def vendas_e_custos(vendas: pd.DataFrame, custos: pd.DataFrame):

    vendas_custos = vendas.merge(
        custos,
        on="id_produto",
        how="left"
    )

    return vendas_custos

def vendas_e_clientes_atualizado(vendas: pd.DataFrame, clientes_atualizado: pd.DataFrame):

    vendas_clientes_atualizado = vendas.merge(
        clientes_atualizado,
        on="id_cliente",
        how="left"
    )

    return vendas_clientes_atualizado

def clientes_e_campanhas(clientes: pd.DataFrame, campanhas: pd.DataFrame):

    vendas_campanhas = clientes.merge(
        campanhas,
        left_on="fonte_aquisicao",
        right_on="canal",
        how="left"
    )

    # 2. Tratar nulos para garantir que nada fique 'vazio'
    # Se o canal for nulo
    vendas_campanhas['canal'] = vendas_campanhas['canal'].fillna('Sem Campanha Ativa')
                
    # Define um ID padrão para quem não veio de campanha paga
    vendas_campanhas['id_campanha'] = vendas_campanhas['id_campanha'].fillna('MKT_OUTROS')
                
    # Investimento nulo vira 0 (essencial para cálculos matemáticos posteriores)
    vendas_campanhas['investimento'] = vendas_campanhas['investimento'].fillna(0)
                
    # Referência de campanha vira 'Orgânico'
    vendas_campanhas['ref'] = vendas_campanhas['ref'].fillna('Sem Campanha / Orgânico')

    return vendas_campanhas