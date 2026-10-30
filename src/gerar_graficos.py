"""
Módulo de Visualização Científica - Gráficos de ITGU, Qualidade do Ar e Desempenho Zootécnico
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

GRAFICOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "graficos")
DADOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados")

def gerar_todos_graficos(dados_dir: str = DADOS_DIR, graficos_dir: str = GRAFICOS_DIR):
    os.makedirs(graficos_dir, exist_ok=True)
    df_leituras = pd.read_csv(os.path.join(dados_dir, "leituras_sensores_iot.csv"))
    df_zoo = pd.read_csv(os.path.join(dados_dir, "comparativo_zootecnico_ge_vs_gc.csv"))

    plt.rcParams["figure.dpi"] = 150
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Gráfico de Evolução do ITGU (GE vs GC)
    fig, ax = plt.subplots(figsize=(10, 5))
    ge_itgu = df_leituras[df_leituras["grupo"] == "GE_Automatizado"].groupby("dia_ciclo")["itgu"].mean()
    gc_itgu = df_leituras[df_leituras["grupo"] == "GC_Convencional"].groupby("dia_ciclo")["itgu"].mean()
    ax.plot(ge_itgu.index, ge_itgu.values, label="Grupo Experimental (Automação Híbrida Python)", color="#00645A", linewidth=2.2)
    ax.plot(gc_itgu.index, gc_itgu.values, label="Grupo Controle (Manejo Convencional)", color="#FF5B00", linestyle="--", linewidth=2.0)
    ax.axhline(74.0, color="#D9534F", linestyle=":", label="Limite Superior de Conforto Térmico (ITGU = 74)")
    ax.set_title("Monitoramento do ITGU ao Longo do Ciclo Produtivo (75 Dias)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Dia do Ciclo de Criação")
    ax.set_ylabel("Índice de Temperatura de Globo e Umidade (ITGU)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "01_evolucao_itgu_ge_vs_gc.png"))
    plt.close()

    # 2. Gráfico de Controle de Gases (Amônia NH3 e CO2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ge_nh3 = df_leituras[df_leituras["grupo"] == "GE_Automatizado"].groupby("dia_ciclo")["nh3_ppm"].mean()
    gc_nh3 = df_leituras[df_leituras["grupo"] == "GC_Convencional"].groupby("dia_ciclo")["nh3_ppm"].mean()
    ax1.plot(ge_nh3.index, ge_nh3.values, label="GE (Automação IoT)", color="#009999", linewidth=2)
    ax1.plot(gc_nh3.index, gc_nh3.values, label="GC (Convencional)", color="#E65100", linestyle="--", linewidth=2)
    ax1.axhline(20.0, color="red", linestyle=":", label="Limite Crítico NH3 (20 ppm)")
    ax1.set_title("Concentração de Amônia (NH3)", fontweight="bold")
    ax1.set_xlabel("Dia do Ciclo")
    ax1.set_ylabel("NH3 (ppm)")
    ax1.legend()

    ge_co2 = df_leituras[df_leituras["grupo"] == "GE_Automatizado"].groupby("dia_ciclo")["co2_ppm"].mean()
    gc_co2 = df_leituras[df_leituras["grupo"] == "GC_Convencional"].groupby("dia_ciclo")["co2_ppm"].mean()
    ax2.plot(ge_co2.index, ge_co2.values, label="GE (Automação IoT)", color="#0B1221", linewidth=2)
    ax2.plot(gc_co2.index, gc_co2.values, label="GC (Convencional)", color="#FF5B00", linestyle="--", linewidth=2)
    ax2.axhline(3000.0, color="red", linestyle=":", label="Limite Crítico CO2 (3000 ppm)")
    ax2.set_title("Concentração de Dióxido de Carbono (CO2)", fontweight="bold")
    ax2.set_xlabel("Dia do Ciclo")
    ax2.set_ylabel("CO2 (ppm)")
    ax2.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "02_qualidade_gasosa_nh3_co2.png"))
    plt.close()

    # 3. Gráfico de Desempenho Zootécnico (Ganho de Peso e Conversão Alimentar)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ge_z = df_zoo[df_zoo["grupo"] == "GE_Automatizado"]
    gc_z = df_zoo[df_zoo["grupo"] == "GC_Convencional"]
    ax1.plot(ge_z["dia_ciclo"], ge_z["peso_medio_g"], marker="o", label="GE (Automação IoT)", color="#00645A", linewidth=2)
    ax1.plot(gc_z["dia_ciclo"], gc_z["peso_medio_g"], marker="s", label="GC (Convencional)", color="#FF5B00", linestyle="--", linewidth=2)
    ax1.set_title("Curva de Ganho de Peso Médio (GPM)", fontweight="bold")
    ax1.set_xlabel("Idade das Aves (Dias)")
    ax1.set_ylabel("Peso Médio (g)")
    ax1.legend()

    ax2.bar(ge_z["semana"] - 0.18, ge_z["conversao_alimentar"], width=0.35, label="GE (Automação IoT)", color="#009999")
    ax2.bar(gc_z["semana"] + 0.18, gc_z["conversao_alimentar"], width=0.35, label="GC (Convencional)", color="#FF5B00")
    ax2.set_title("Evolução da Conversão Alimentar (CA - Menor é Melhor)", fontweight="bold")
    ax2.set_xlabel("Semana do Ciclo")
    ax2.set_ylabel("Conversão Alimentar (kg ração / kg peso)")
    ax2.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "03_desempenho_zootecnico_gpm_ca.png"))
    plt.close()

    # 4. Eficiência Energética e Mortalidade
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.plot(ge_z["dia_ciclo"], ge_z["consumo_energia_acumulado_kwh"], marker="o", label="GE (Controle Adaptativo PID)", color="#00645A", linewidth=2)
    ax1.plot(gc_z["dia_ciclo"], gc_z["consumo_energia_acumulado_kwh"], marker="s", label="GC (Acionamento Manual/Fixo)", color="#D9534F", linestyle="--", linewidth=2)
    ax1.set_title("Consumo Energético Acumulado (Redução de ~36.8%)", fontweight="bold")
    ax1.set_xlabel("Dias de Ciclo")
    ax1.set_ylabel("Consumo Acumulado (kWh)")
    ax1.legend()

    ax2.plot(ge_z["dia_ciclo"], ge_z["mortalidade_acumulada_pct"], marker="o", label="GE (Automação IoT)", color="#009999", linewidth=2)
    ax2.plot(gc_z["dia_ciclo"], gc_z["mortalidade_acumulada_pct"], marker="s", label="GC (Convencional)", color="#E65100", linestyle="--", linewidth=2)
    ax2.set_title("Taxa de Mortalidade Acumulada (%)", fontweight="bold")
    ax2.set_xlabel("Dias de Ciclo")
    ax2.set_ylabel("Mortalidade (%)")
    ax2.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "04_eficiencia_energetica_mortalidade.png"))
    plt.close()
