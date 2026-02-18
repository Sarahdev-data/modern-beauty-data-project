import pandas as pd
from scripts.data_loader import load_vendas, load_produtos, load_custos, load_clientes_atualizado, load_campanhas_marketing
from scripts.data_cleaning import clean_vendas, clean_produtos, clean_custos, clean_clientes_atualizado, clean_campanhas_marketing
from scripts.data_merging import vendas_e_produtos, vendas_e_custos, vendas_e_clientes_atualizado, clientes_e_campanhas
from scripts.data_modeling import métricas_vendas


def main():
    print("Iniciando pipeline de dados...\n")

    #1.LOAD

    vendas = load_vendas()
    produtos = load_produtos()
    custos = load_custos()
    clientes = load_clientes_atualizado()
    campanhas = load_campanhas_marketing()

    # Verificação básica
    if any(df is None for df in [vendas, produtos, custos, clientes, campanhas]):
        raise ValueError("Um ou mais arquivos não foram carregados corretamente.")
    
    #2.CLEAN

    vendas = clean_vendas(vendas)
    produtos = clean_produtos(produtos)
    custos = clean_custos(custos)
    clientes = clean_clientes_atualizado(clientes)
    campanhas = clean_campanhas_marketing(campanhas)

    print("Limpeza concluída!")

    #3.MERGE

    vendas = vendas_e_produtos(vendas, produtos)
    vendas = vendas_e_custos(vendas, custos)
    vendas = vendas_e_clientes_atualizado(vendas, clientes)
    clientes_campanhas = clientes_e_campanhas(clientes, campanhas)

    print("Merges concluídos!")

    #4.MÉTRICAS

    vendas = métricas_vendas(vendas)
    print("Métricas criadas com sucesso!")

    #5.SALVAR CSV

    vendas.to_csv("data/processed/modern_beauty_vendas.csv", index=False)
    clientes_campanhas.to_csv("data/processed/modern_beauty_clientes_campanhas.csv", index=False)
    print("CSVs salvos em data/processed/ \n")

    #6.FINAL

    print("\n Preview do DataFrame final:")
    print(vendas.head())
    
    print("\n Preview clientes + campanhas:")
    print(clientes_campanhas.head())
 
    print("\n Pipeline finalizado com sucesso!")


if __name__ == "__main__":
    main()