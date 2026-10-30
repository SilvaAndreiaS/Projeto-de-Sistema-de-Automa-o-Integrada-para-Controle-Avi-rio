"""
Orquestrador Principal do Gateway IoT (Raspberry Pi) - Aviário Inteligente G001
Executa a simulação de 75 dias de ciclo produtivo (4.000 aves em 360 m² - 12m x 30m),
gravando no banco SQLite, exportando CSVs e gerando os gráficos de validação.
"""
import random
from datetime import datetime, timedelta
from calculo_itgu import calcular_temperatura_ponto_orvalho, estimar_temperatura_globo_negro, calcular_itgu
from sensores import validar_mapeamento
from controle_automatico import ControladorHibridoAviario
from banco_dados import inicializar_banco, inserir_leitura, DB_DEFAULT_PATH
from exportar_csv import exportar_tabelas_para_csv
from gerar_graficos import gerar_todos_graficos
import sqlite3

def executar_simulacao_completa():
    print("==================================================================")
    print(" INICIANDO SISTEMA DE AUTOMAÇÃO HÍBRIDA IoT - AVIÁRIO G001 (UFMT) ")
    print("==================================================================")
    inicializar_banco()
    controlador = ControladorHibridoAviario(itgu_setpoint=72.0)

    random.seed(42)
    data_inicio = datetime(2025, 9, 1, 12, 0, 0)

    # Limpar dados anteriores para execução limpa
    conn = sqlite3.connect(DB_DEFAULT_PATH)
    conn.execute("DELETE FROM leituras_ambientais")
    conn.execute("DELETE FROM desempenho_zootecnico")
    conn.commit()

    # Simular leituras diárias ao longo de 75 dias para Grupo Experimental (GE) e Grupo Controle (GC)
    for dia in range(1, 76):
        ts = (data_inicio + timedelta(days=dia - 1)).strftime("%Y-%m-%d %H:%M:%S")
        # Temperatura externa base sazonal em MT
        temp_externa = 30.5 + random.uniform(-2.0, 4.5)
        ur_externa = 68.0 + random.uniform(-8.0, 12.0)

        # 1. Grupo Experimental (Com Automação Híbrida Python + Fog Computing)
        ta_ge = temp_externa - random.uniform(3.2, 5.0)
        ur_ge = min(72.0, max(52.0, ur_externa - random.uniform(3.0, 8.0)))
        nh3_ge = 5.0 + (dia * 0.11) + random.uniform(-1.0, 1.5)
        co2_ge = 750.0 + (dia * 12.0) + random.uniform(-80.0, 90.0)

        valid_ge = validar_mapeamento("ESP32_Norte", ta_ge, ur_ge, nh3_ge, co2_ge)
        tpo_ge = calcular_temperatura_ponto_orvalho(ta_ge, ur_ge)
        tg_ge = estimar_temperatura_globo_negro(ta_ge, ur_ge)
        itgu_ge = calcular_itgu(tg_ge, tpo_ge)
        atuacao_ge = controlador.calcular_atuacao(itgu_ge, ur_ge, nh3_ge, co2_ge)

        inserir_leitura({
            "timestamp": ts, "dia_ciclo": dia, "grupo": "GE_Automatizado", "sensor_id": "ESP32_Norte",
            "temperatura_c": round(ta_ge, 2), "umidade_relativa": round(ur_ge, 2),
            "tg_c": tg_ge, "tpo_c": tpo_ge, "itgu": itgu_ge,
            "nh3_ppm": round(nh3_ge, 2), "co2_ppm": round(co2_ge, 1),
            "velocidade_ar_ms": atuacao_ge["velocidade_ar_ms"],
            "potencia_exaustores_pct": atuacao_ge["potencia_exaustores_pct"],
            "nebulizador_ativo": atuacao_ge["nebulizador_ativo"],
            "consumo_kwh": round(atuacao_ge["consumo_estimado_kw"] * 14.0, 2)
        })

        # 2. Grupo Controle (Manejo Convencional Manual)
        ta_gc = temp_externa - random.uniform(0.5, 1.8)
        ur_gc = min(86.0, max(60.0, ur_externa + random.uniform(0.0, 6.0)))
        nh3_gc = 8.0 + (dia * 0.28) + random.uniform(-1.5, 3.0)
        co2_gc = 1050.0 + (dia * 29.0) + random.uniform(-100.0, 180.0)

        tpo_gc = calcular_temperatura_ponto_orvalho(ta_gc, ur_gc)
        tg_gc = estimar_temperatura_globo_negro(ta_gc, ur_gc)
        itgu_gc = calcular_itgu(tg_gc, tpo_gc)

        inserir_leitura({
            "timestamp": ts, "dia_ciclo": dia, "grupo": "GC_Convencional", "sensor_id": "ESP32_Sul_GC",
            "temperatura_c": round(ta_gc, 2), "umidade_relativa": round(ur_gc, 2),
            "tg_c": tg_gc, "tpo_c": tpo_gc, "itgu": itgu_gc,
            "nh3_ppm": round(nh3_gc, 2), "co2_ppm": round(co2_gc, 1),
            "velocidade_ar_ms": 1.1, "potencia_exaustores_pct": 100.0,
            "nebulizador_ativo": 0, "consumo_kwh": round(1.85 * 18.5, 2)
        })

    # Inserir resumo semanal zootécnico (11 avaliações até 75 dias)
    semanas_dias = [(1, 7), (2, 14), (3, 21), (4, 28), (5, 35), (6, 42), (7, 49), (8, 56), (9, 63), (10, 70), (11, 75)]
    cursor = conn.cursor()
    for sem, d in semanas_dias:
        peso_ge = round(45.0 + (d ** 1.48) * 4.65, 1)
        peso_gc = round(45.0 + (d ** 1.45) * 4.35, 1)
        ca_ge = round(1.15 + (d * 0.0125), 2)
        ca_gc = round(1.22 + (d * 0.0155), 2)
        mort_ge = round(0.25 + (d * 0.022), 2)
        mort_gc = round(0.45 + (d * 0.062), 2)
        kwh_ge = round(d * 21.4, 1)
        kwh_gc = round(d * 33.9, 1)

        cursor.execute("""
            INSERT INTO desempenho_zootecnico (semana, dia_ciclo, grupo, peso_medio_g, conversao_alimentar, mortalidade_acumulada_pct, consumo_energia_acumulado_kwh)
            VALUES (?, ?, 'GE_Automatizado', ?, ?, ?, ?)
        """, (sem, d, peso_ge, ca_ge, mort_ge, kwh_ge))

        cursor.execute("""
            INSERT INTO desempenho_zootecnico (semana, dia_ciclo, grupo, peso_medio_g, conversao_alimentar, mortalidade_acumulada_pct, consumo_energia_acumulado_kwh)
            VALUES (?, ?, 'GC_Convencional', ?, ?, ?, ?)
        """, (sem, d, peso_gc, ca_gc, mort_gc, kwh_gc))

    conn.commit()
    conn.close()

    csv1, csv2 = exportar_tabelas_para_csv()
    gerar_todos_graficos()
    print(f"[OK] Banco SQLite populado: {DB_DEFAULT_PATH}")
    print(f"[OK] CSVs exportados: {csv1} | {csv2}")
    print("[OK] Gráficos de validação gerados na pasta graficos/.")

if __name__ == "__main__":
    executar_simulacao_completa()
