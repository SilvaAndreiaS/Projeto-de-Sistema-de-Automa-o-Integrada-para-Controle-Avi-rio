"""
Módulo de Persistência Local (SQLite) no Gateway Raspberry Pi (Fog Computing)
Armazena leituras ambientais, ITGU, estados dos atuadores e métricas zootécnicas.
"""
import sqlite3
import os

DB_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados", "aviario_iot.db")

def inicializar_banco(db_path: str = DB_DEFAULT_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras_ambientais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            dia_ciclo INTEGER NOT NULL,
            grupo TEXT NOT NULL,
            sensor_id TEXT NOT NULL,
            temperatura_c REAL NOT NULL,
            umidade_relativa REAL NOT NULL,
            tg_c REAL NOT NULL,
            tpo_c REAL NOT NULL,
            itgu REAL NOT NULL,
            nh3_ppm REAL NOT NULL,
            co2_ppm REAL NOT NULL,
            velocidade_ar_ms REAL NOT NULL,
            potencia_exaustores_pct REAL NOT NULL,
            nebulizador_ativo INTEGER NOT NULL,
            consumo_kwh REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desempenho_zootecnico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana INTEGER NOT NULL,
            dia_ciclo INTEGER NOT NULL,
            grupo TEXT NOT NULL,
            peso_medio_g REAL NOT NULL,
            conversao_alimentar REAL NOT NULL,
            mortalidade_acumulada_pct REAL NOT NULL,
            consumo_energia_acumulado_kwh REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_leitura(registro: dict, db_path: str = DB_DEFAULT_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leituras_ambientais (
            timestamp, dia_ciclo, grupo, sensor_id, temperatura_c, umidade_relativa,
            tg_c, tpo_c, itgu, nh3_ppm, co2_ppm, velocidade_ar_ms,
            potencia_exaustores_pct, nebulizador_ativo, consumo_kwh
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        registro["timestamp"], registro["dia_ciclo"], registro["grupo"], registro["sensor_id"],
        registro["temperatura_c"], registro["umidade_relativa"], registro["tg_c"], registro["tpo_c"],
        registro["itgu"], registro["nh3_ppm"], registro["co2_ppm"], registro["velocidade_ar_ms"],
        registro["potencia_exaustores_pct"], int(registro["nebulizador_ativo"]), registro["consumo_kwh"]
    ))
    conn.commit()
    conn.close()
