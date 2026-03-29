from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# schemas → define estrutura dos dados
# validators → aplica schemas em DataFrames
# main → chama a validação no pipeline

class VendaSchemas(BaseModel):
    id_venda:str
    data_venda:datetime
    id_cliente:str
    id_produto:str
    quantidade:int
    forma_pagamento:str

class ProdutoSchemas(BaseModel):
    id_produto:str
    nome_produto:str
    categoria:str
    marca:str
    volume_ml:Optional[float] = None # Aceita valores nulos
    preco_unitario:float = Field(gt=0)  # Valor deve ser maior que zero
    ativo:str

class CustoSchemas(BaseModel):
    id_produto:str
    custo_unitario:float = Field(gt=0)
    fornecedor:str

class ClienteSchemas(BaseModel):
    id_cliente:str
    nome_cliente:str
    email:str
    sexo:str
    data_nascimento:datetime
    cidade:str
    estado:str
    data_cadastro:datetime
    fonte_aquisicao:str

class CampanhaSchemas(BaseModel):
    id_campanha:str
    canal:str
    data_inicio:datetime
    data_fim:datetime
    investimento:float
    ref:str