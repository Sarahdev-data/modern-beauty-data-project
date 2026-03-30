import logging

def save_to_mysql(df, table_name, engine, if_exists="replace"):
    try:
        df.to_sql(
            name = table_name,
            con = engine,
            if_exists = if_exists,
            index = False
        )
        logging.info(f"Tabela '{table_name}' salva com sucesso no MySql!")
    
    except Exception as e:
        logging.error(f"Erro ao salvar tabela '{table_name}': {e}")
        raise