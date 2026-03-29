import pandas as pd
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
 
def load_csv(filename: str) -> pd.DataFrame | None:
    file_path = RAW_DIR / filename
    try:
        df = pd.read_csv(file_path)
        logging.info(f"{filename} carregado com sucesso!")
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar {filename}: {e}")
        return None


def load_vendas() -> pd.DataFrame | None:
    return load_csv("vendas.csv")

def load_produtos() -> pd.DataFrame | None:
    return load_csv("produtos.csv")

def load_custos() -> pd.DataFrame | None:
    return load_csv("custos.csv")

def load_clientes_atualizado() -> pd.DataFrame | None:
    return load_csv("clientes_atualizado.csv")

def load_campanhas_marketing() -> pd.DataFrame | None:
    return load_csv("campanhas_marketing.csv")