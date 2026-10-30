"""
Módulo de Cálculo Bioclimático - Índice de Temperatura de Globo e Umidade (ITGU)
Curso de Pós-Graduação em Agrocomputação - UFMT
Autores: Andreia Souza S. da Silva, Cristiano Cruz, Elienai Cardoso, Kenedy Cruz, Wagner
"""
import math

def calcular_temperatura_ponto_orvalho(ta: float, ur: float) -> float:
    """
    Calcula a temperatura do ponto de orvalho (Tpo) em °C usando a fórmula de Magnus-Tetens.
    :param ta: Temperatura do ar (bulbo seco) em °C
    :param ur: Umidade relativa em % (0 a 100)
    """
    ur_clamped = max(1.0, min(100.0, ur))
    a = 17.27
    b = 237.7
    alfa = ((a * ta) / (b + ta)) + math.log(ur_clamped / 100.0)
    tpo = (b * alfa) / (a - alfa)
    return round(tpo, 2)

def estimar_temperatura_globo_negro(ta: float, ur: float, rad_solar: float = 0.0) -> float:
    """
    Estima a Temperatura de Globo Negro (Tg) com base na temperatura ambiente (Ta)
    e carga térmica radiante interna do galpão avícola.
    """
    incremento_radiante = 1.5 if rad_solar == 0.0 else (rad_solar * 0.005)
    return round(ta + incremento_radiante, 2)

def calcular_itgu(tg: float, tpo: float) -> float:
    """
    Calcula o Índice de Temperatura de Globo e Umidade (ITGU) segundo Buffington et al. (1981).
    Fórmula oficial: ITGU = Tg + 0.36 * Tpo + 41.5
    """
    itgu = tg + (0.36 * tpo) + 41.5
    return round(itgu, 2)

def classificar_conforto_termico(itgu: float, semana_vida: int = 5) -> dict:
    """
    Classifica a condição térmica das aves com base no ITGU e na idade do lote.
    Faixas de referência (Abreu & Abreu, 2011; Baêta & Souza, 2010).
    """
    # Limites superiores de conforto térmico por semana de vida
    limites = {1: 80.0, 2: 77.0, 3: 75.0, 4: 74.0, 5: 73.0, 6: 72.0}
    limite_conforto = limites.get(min(max(semana_vida, 1), 6), 72.0)

    if itgu < (limite_conforto - 4.0):
        status = "ESTRESSE_FRIO"
        acao_recomendada = "Fechar cortinas, desligar exaustores e acionar aquecimento se necessário."
    elif itgu <= limite_conforto:
        status = "CONFORTO_TERMICO"
        acao_recomendada = "Manter ventilação mínima higiênica e lanternim aberto."
    elif itgu <= (limite_conforto + 3.0):
        status = "ALERTA_MODERADO"
        acao_recomendada = "Incrementar velocidade do ar (VA) gradualmente e abrir cortinas."
    else:
        status = "ESTRESSE_CALORICO_CRITICO"
        acao_recomendada = "Acionar exaustores em potência máxima (VA > 2.5 m/s) e ligar nebulização."

    return {
        "itgu": itgu,
        "limite_referencia": limite_conforto,
        "status": status,
        "acao_recomendada": acao_recomendada
    }

if __name__ == "__main__":
    ta_teste, ur_teste = 31.5, 72.0
    tpo = calcular_temperatura_ponto_orvalho(ta_teste, ur_teste)
    tg = estimar_temperatura_globo_negro(ta_teste, ur_teste)
    itgu = calcular_itgu(tg, tpo)
    avaliacao = classificar_conforto_termico(itgu, semana_vida=6)
    print(f"Teste ITGU -> Ta: {ta_teste}°C | UR: {ur_teste}% | Tg: {tg}°C | Tpo: {tpo}°C | ITGU: {itgu}")
    print(f"Classificação: {avaliacao['status']} - {avaliacao['acao_recomendada']}")
