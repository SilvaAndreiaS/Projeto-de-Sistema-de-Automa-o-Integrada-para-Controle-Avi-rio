"""
Módulo de Exportação de Dados e Relatórios Analíticos (CSV)
Converte registros do SQLite em planilhas CSV para validação estatística (Grupo Experimental vs Controle).
"""
import sqlite3
import pandas as pd
import os
from banco_dados import DB_DEFAULT_PATH

DADOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados")

def exportar_tabelas_para_csv(db_path: str = DB_DEFAULT_PATH, output_dir: str = DADOS_DIR):
    os.makedirs(output_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)

    df_leituras = pd.read_sql_query("SELECT * FROM leituras_ambientais", conn)
    csv_leituras = os.path.join(output_dir, "leituras_sensores_iot.csv")
    df_leituras.to_csv(csv_leituras, index=False, encoding="utf-8")

    df_zoo = pd.read_sql_query("SELECT * FROM desempenho_zootecnico", conn)
    csv_zoo = os.path.join(output_dir, "comparativo_zootecnico_ge_vs_gc.csv")
    df_zoo.to_csv(csv_zoo, index=False, encoding="utf-8")

    conn.close()
    return csv_leituras, csv_zoo
