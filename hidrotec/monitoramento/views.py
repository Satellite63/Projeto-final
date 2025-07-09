from django.shortcuts import render, redirect
from db_utils import execute_sql
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

def dashboard_estoque():
    query = """
        SELECT 
            SUM(a.valor_estoque),
            a.tipo
        FROM(
                SELECT 
                    id_estoque,
                    nome_estoque,
                    categoria,
                    quantidade_estoque,
                    valor_estoque,
                    dt_entrada_estoque,
                    dt_validade_estoque,
                    CASE WHEN valor_estoque >= 0 THEN 'saldo' ELSE 'prejuizo' END as tipo
                FROM estoque
                WHERE categoria = 'Plantio'
            ) as A
            group by tipo
    """
    produtos = execute_sql(query, {}, False)
    return produtos

def gerar_grafico_tipo():
    query = """
        SELECT 
            SUM(a.valor_estoque),
            Count(a.id_estoque),
            a.tipo
        FROM(
                SELECT 
                    id_estoque,
                    nome_estoque,
                    categoria,
                    quantidade_estoque,
                    valor_estoque,
                    dt_entrada_estoque,
                    dt_validade_estoque,
                    CASE WHEN valor_estoque >= 0 THEN 'saldo' ELSE 'prejuizo' END as tipo
                FROM estoque
                WHERE categoria = 'Plantio'
            ) as A
            group by tipo
    """
    # Executar a query
    produtos = execute_sql(query, {}, False) 
    return produtos