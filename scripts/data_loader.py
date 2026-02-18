import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
 
def load_csv(filename):
    file_path = RAW_DIR / filename
    try:
        df = pd.read_csv(file_path)
        print(f"{filename} carregado com sucesso!")
        return df
    except:
        print(f"{filename} não encontrado em {RAW_DIR}")
        return None


def load_vendas():
    return load_csv("vendas.csv")

def load_produtos():
    return load_csv("produtos.csv")

def load_custos():
    return load_csv("custos.csv")

def load_clientes_atualizado():
    return load_csv("clientes_atualizado.csv")

def load_campanhas_marketing():
    return load_csv("campanhas_marketing.csv")