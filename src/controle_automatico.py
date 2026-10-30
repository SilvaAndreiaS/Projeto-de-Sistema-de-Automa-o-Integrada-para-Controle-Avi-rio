"""
Módulo de Controle Automático Híbrido (PID / Lógica Fuzzy) em Fog Computing (Raspberry Pi)
Modula Velocidade do Ar (VA), abertura de cortinas, nebulizadores e renovação gasosa.
"""

class ControladorHibridoAviario:
    def __init__(self, itgu_setpoint: float = 72.0, nh3_limite: float = 20.0, co2_limite: float = 3000.0):
        self.itgu_setpoint = itgu_setpoint
        self.nh3_limite = nh3_limite
        self.co2_limite = co2_limite
        self.kp = 12.5
        self.ki = 1.8
        self.kd = 3.2
        self.erro_acumulado = 0.0
        self.erro_anterior = 0.0

    def calcular_atuacao(self, itgu_atual: float, ur_atual: float, nh3_ppm: float, co2_ppm: float) -> dict:
        """
        Determina o estado dos atuadores priorizando segurança sanitária (gases) e conforto térmico (ITGU).
        """
        erro_itgu = itgu_atual - self.itgu_setpoint
        self.erro_acumulado = max(-10.0, min(10.0, self.erro_acumulado + erro_itgu))
        derivada_erro = erro_itgu - self.erro_anterior
        self.erro_anterior = erro_itgu

        # Saída PID para potência dos exaustores (0 a 100%)
        sinal_pid = (self.kp * erro_itgu) + (self.ki * self.erro_acumulado) + (self.kd * derivada_erro)
        potencia_exaustores = max(15.0, min(100.0, round(sinal_pid, 1))) if erro_itgu > 0 else 15.0

        # Prioridade 1: Qualidade Gasosa (NH3 > 20 ppm ou CO2 > 3000 ppm)
        alerta_gases = (nh3_ppm >= self.nh3_limite) or (co2_ppm >= self.co2_limite)
        if alerta_gases:
            potencia_exaustores = max(potencia_exaustores, 85.0)
            modo_operacao = "EMERGENCIA_SANITARIA_GASES"
        elif erro_itgu > 3.5:
            modo_operacao = "RESFRIAMENTO_ CONVECTIVO_MAXIMO"
        elif erro_itgu > 0.5:
            modo_operacao = "MODULACAO_ADAPTATIVA_PID"
        else:
            modo_operacao = "VENTILACAO_MINIMA_LANTERNIM"

        # Velocidade do Ar estimada (0.3 m/s a 3.0 m/s)
        velocidade_ar_ms = round(0.3 + (potencia_exaustores / 100.0) * 2.7, 2)

        # Nebulização só liga se ITGU estiver alto E umidade relativa permitir (< 75%)
        nebulizador_ativo = (itgu_atual > (self.itgu_setpoint + 2.5)) and (ur_atual < 75.0)

        # Posição das cortinas (0% = fechada, 100% = totalmente aberta para ventilação natural/mista)
        abertura_cortinas_pct = 100 if (itgu_atual > self.itgu_setpoint or alerta_gases) else 35

        # Estimativa de consumo elétrico instantâneo (kW) - Eficiência da modulação híbrida
        consumo_kw = round((potencia_exaustores / 100.0) * 1.85 + (0.45 if nebulizador_ativo else 0.0), 3)

        return {
            "modo_operacao": modo_operacao,
            "potencia_exaustores_pct": potencia_exaustores,
            "velocidade_ar_ms": velocidade_ar_ms,
            "nebulizador_ativo": nebulizador_ativo,
            "abertura_cortinas_pct": abertura_cortinas_pct,
            "alerta_gases": alerta_gases,
            "consumo_estimado_kw": consumo_kw
        }
