import pytest
import pandas as pd
import logging
from typing import Callable, Type
from pydantic import BaseModel
from scripts.data_loader import load_vendas, load_custos, load_produtos, load_clientes_atualizado, load_campanhas_marketing
from schemas.schemas import VendaSchemas, CustoSchemas, ProdutoSchemas, ClienteSchemas, CampanhaSchemas

# Mapeamento para facilitar o parametrize: (função_loader, schema_pydantic, nome_legível)
TABELAS_PARA_VALIDAR = [
    (load_vendas, VendaSchemas, "Vendas"),
    (load_custos, CustoSchemas, "Custos"),
    (load_produtos, ProdutoSchemas, "Produtos"),
    (load_clientes_atualizado, ClienteSchemas, "Clientes"),
    (load_campanhas_marketing, CampanhaSchemas, "Campanhas")
]


@pytest.mark.parametrize("loader_func, schema, nome_tabela", TABELAS_PARA_VALIDAR)
def test_check_required_columns(loader_func: Callable[[], pd.DataFrame], schema: Type[BaseModel], nome_tabela: str) -> None :
    """
    Verifica se todas as colunas obrigatórias definidas no Pydantic estão presentes nos arquivos CSV carregados.
    """
    # 1. Carrega os dados reais usando funções do data_loader
    df = loader_func()

    # Garantia básica que o arquivo foi lido
    assert df is not None, f"Falha ao carregar {nome_tabela}. O DataFrame retornou None."

    # 2. Extrai as colunas esperadas do Schema do Pydantic
    # .model_fields retorna um dicionário com todos os campos da classe
    colunas_esperadas = set(schema.model_fields.keys())
    colunas_reais = set(df.columns)

    # 3. Identifica quais colunas estão faltando
    colunas_faltantes = colunas_esperadas - colunas_reais
    
    # 4. Assert com mensagem detalhada em caso de erro
    assert not colunas_faltantes, (
        f"A tabela '{nome_tabela}' está incompleta!\n"
        f"Colunas ausentes: {colunas_faltantes}\n"
        f"Colunas encontradas no arquivo: {list(colunas_reais)}"
    )


"""
Teste para avisar se existem colunas no CSV que não estão mapeadas no Pydantic.
"""
@pytest.mark.parametrize("loader_func, schema, nome_tabela", TABELAS_PARA_VALIDAR)
def test_check_extra_columns(loader_func: Callable[[], pd.DataFrame], schema: Type[BaseModel], nome_tabela: str) -> None:
    """
    Avisa via log se existem colunas no CSV que não foram mapeadas no Schema do Pydantic.
    """
    df = loader_func()
    
    assert df is not None, f"Falha ao carregar {nome_tabela}."

    colunas_esperadas = set(schema.model_fields.keys())
    colunas_reais = set(df.columns)
    
    colunas_extras = colunas_reais - colunas_esperadas
    
    if colunas_extras:
        logging.warning(f"\n[Aviso] A tabela '{nome_tabela}' possui colunas extras não mapeadas: {colunas_extras}")