import pytest
import pandas as pd
from typing import Callable, Optional
from unittest.mock import patch
from scripts.data_loader import load_csv, load_vendas, load_produtos, load_custos, load_clientes_atualizado, load_campanhas_marketing, RAW_DIR

@pytest.fixture
def mock_dataframe() -> pd.DataFrame:
    return pd.DataFrame({
        "col1":[1,2],
        "col2":[3,4]
    })

# Teste de Falha: Quando o arquivo não existe
def test_load_csv_file_not_found() -> None:
    # Simula que o read_csv levanta um erro de arquivo não encontrado
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result: Optional[pd.DataFrame] = load_csv("arquivo_fake.csv")
        assert result is None

# Teste de Sucesso: Simulando o carregamento de um DataFrame
def test_load_csv_success(mock_dataframe: pd.DataFrame) -> None:
    with patch("pandas.read_csv", return_value=mock_dataframe):
        df: Optional[pd.DataFrame] = load_csv("teste.csv")
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert list(df.columns) == ["col1", "col2"]

#Verifica se a função não retornou None.
#Verifica se o retorno é um DataFrame do pandas.
#Verifica se o DataFrame não está vazio.
@pytest.mark.parametrize(
    "function, filename",
    [
        (load_vendas,"vendas.csv"),
        (load_produtos,"produtos.csv"),
        (load_custos,"custos.csv"),
        (load_clientes_atualizado,"clientes_atualizado.csv"),
        (load_campanhas_marketing,"campanhas_marketing.csv"),
    ],
)
def test_load_functions(function: Callable[[], pd.DataFrame], filename: str) -> None:
    """ 'function' recebe um Callable (função sem argumentos que retorna DataFrame). """
    df: pd.DataFrame = function()
    assert df is not None, f"{filename} não foi carregado"
    assert isinstance(df, pd.DataFrame), f"{filename} não retornou DataFrame"
    assert not df.empty, f"{filename} está vazio"

#Verificar se o read_csv foi chamado com o caminho correto.
@pytest.mark.parametrize(
    "function, filename",
    [
        (load_vendas,"vendas.csv"),
        (load_produtos,"produtos.csv"),
        (load_custos,"custos.csv"),
        (load_clientes_atualizado,"clientes_atualizado.csv"),
        (load_campanhas_marketing,"campanhas_marketing.csv"),
    ],
)
def test_loader_calls_correct_file(function: Callable[[], pd.DataFrame], filename: str) -> None:
    with patch("pandas.read_csv") as mock_read:
        function()
        mock_read.assert_called_once_with(RAW_DIR / filename)