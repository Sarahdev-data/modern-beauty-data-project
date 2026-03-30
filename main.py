import pandas as pd
import logging
from database.connection import get_engine
from database.writer import save_to_mysql
from pathlib import Path
from schemas.schemas import VendaSchemas, ProdutoSchemas, CustoSchemas, ClienteSchemas, CampanhaSchemas
from scripts.data_loader import load_vendas, load_produtos, load_custos, load_clientes_atualizado, load_campanhas_marketing
from scripts.data_cleaning import clean_vendas, clean_produtos, clean_custos, clean_clientes_atualizado, clean_campanhas_marketing
from validators.validators import validate_vendas, validate_produtos, validate_custos, validate_clientes, validate_campanhas
from scripts.data_merging import vendas_e_produtos, vendas_e_custos, vendas_e_clientes_atualizado, clientes_e_campanhas
from scripts.data_modeling import métricas_vendas

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def check_columns(df, schema, name):
    """Verifica se todas as colunas do schema existem no DF."""
    expected = set(schema.model_fields.keys())
    actual = set(df.columns)
    missing = expected - actual
    if missing:
        raise ValueError(f"A tabela {name} está sem as colunas obrigatórias: {missing}")
    
    # Logar colunas extras como aviso (sem interromper)
    extra = actual - expected
    if extra:
        logging.warning(f"A tabela {name} possui colunas extras que serão ignoradas: {extra}")


def main():
    logging.info("Iniciando pipeline de dados...\n")

    #1.LOAD

    try:
        vendas: pd.DataFrame = load_vendas()
        produtos: pd.DataFrame = load_produtos()
        custos: pd.DataFrame = load_custos()
        clientes: pd.DataFrame = load_clientes_atualizado()
        campanhas: pd.DataFrame = load_campanhas_marketing()

        # Verificação básica
        if any(df is None for df in [vendas, produtos, custos, clientes, campanhas]):
            raise ValueError("Um ou mais arquivos não foram carregados corretamente.")
        
        logging.info("Todos os arquivos foram carregados com sucesso!")

    except Exception as e:
        logging.critical(f"Erro no carregamento (LOAD): {e}")
        raise
    
    # 2.CHECK STRUCTURE

    try:
        logging.info("Checando estrutura das colunas...")
        check_columns(vendas, VendaSchemas, "Vendas")
        check_columns(produtos, ProdutoSchemas, "Produtos")
        check_columns(custos, CustoSchemas, "Custos")
        check_columns(clientes, ClienteSchemas, "Clientes")
        check_columns(campanhas, CampanhaSchemas, "Campanhas")
        
        logging.info("Estrutura validada com sucesso!")

    except Exception as e:
        logging.critical(f"Erro na fase de estrutura (CHECK): {e}")
        raise
    
    #3.CLEAN

    try:
        vendas = clean_vendas(vendas)
        produtos = clean_produtos(produtos)
        custos = clean_custos(custos)
        clientes = clean_clientes_atualizado(clientes)
        campanhas = clean_campanhas_marketing(campanhas)

        logging.info("Limpeza concluída!")

    except Exception as e:
        logging.critical(f"Erro ao limpar dados (CLEAN): {e}")
        raise

    #4.VALIDATION

    try:
        logging.info("Iniciando validação...")

        all_errors = []

        validations = {
            "vendas": (vendas, validate_vendas),
            "produtos": (produtos, validate_produtos),
            "custos": (custos, validate_custos),
            "clientes": (clientes, validate_clientes),
            "campanhas": (campanhas, validate_campanhas),
        }

        # Loop dinâmico
        validated_dfs = {}
        for name, (df, func) in validations.items():
            df_validado, err = func(df)
            validated_dfs[name] = df_validado # Guardamos o DF limpo
            
            if not err.empty:
                err["tabela"] = name
                all_errors.append(err)

        # Atualiza as variáveis originais com os dados validados
        vendas = validated_dfs["vendas"]
        produtos = validated_dfs["produtos"]
        custos = validated_dfs["custos"]
        clientes = validated_dfs["clientes"]
        campanhas = validated_dfs["campanhas"]

        # Consolidação dos erros
        if all_errors:
            final_errors = pd.concat(all_errors, ignore_index=True)

            # Garantir que a pasta existe
            Path("data/errors").mkdir(parents=True, exist_ok=True)

            final_errors.to_csv("data/errors/validation_errors.csv", index=False)

            logging.warning(f"{len(final_errors)} erros de validação encontrados!")

        logging.info("Validation concluída!")

    except Exception as e:
        logging.critical(f"Erro em Validation: {e}")
        raise

    #5.MERGE

    try:
        vendas = vendas_e_produtos(vendas, produtos)
        vendas = vendas_e_custos(vendas, custos)
        vendas = vendas_e_clientes_atualizado(vendas, clientes)
        clientes_campanhas = clientes_e_campanhas(clientes, campanhas)

        logging.info("Merges concluídos!")

    except Exception as e:
        logging.critical(f"Erro ao realizar merge (MERGE): {e}")
        raise

    #6.MÉTRICAS

    vendas = métricas_vendas(vendas)
    logging.info("Métricas criadas com sucesso!")

    #7.SALVAR CSV

    # vendas.to_csv("data/processed/modern_beauty_vendas.csv", index=False)
    # clientes_campanhas.to_csv("data/processed/modern_beauty_clientes_campanhas.csv", index=False)
    # logging.info("CSVs salvos em data/processed/ \n")

    # 8.SALVAR NO MYSQL

    try:
        logging.info("Conectando ao banco de dados...")

        engine = get_engine()

        logging.info("Salvando dados no MySQL...")

        save_to_mysql(vendas, "fato_vendas", engine)
        save_to_mysql(clientes_campanhas, "dim_clientes_campanhas", engine)

        logging.info("Dados salvos no MySQL com sucesso!")

    except Exception as e:
        logging.critical(f"Erro ao salvar no banco: {e}")
        raise

    # 9.FINAL

    # logging.info("\n Pipeline finalizado com sucesso! Exibindo previews abaixo: ")

    # print("\n Preview do DataFrame final:")
    # print(vendas.head())
    
    # print("\n Preview clientes + campanhas:")
    # print(clientes_campanhas.head())


if __name__ == "__main__":
    main()