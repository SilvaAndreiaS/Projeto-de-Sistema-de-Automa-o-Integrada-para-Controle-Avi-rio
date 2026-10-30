"""
Módulo de Aquisição e Validação de Nós Sensoriais IoT (ESP32 + DHT22 + MQ-135)
Instalados a 50 cm do piso (zona de ocupação das aves coloniais/corte).
"""
import random
from datetime import datetime

def validar_mapeamento(sensor_id: str, valor_temp: float, valor_umid: float, nh3_ppm: float = 5.0, co2_ppm: float = 800.0) -> dict:
    """
    Verifica se os dados coletados pelos sensores DHT22 e MQ-135 estão dentro de faixas físicas reais.
    """
    erros = []
    if not (10.0 <= valor_temp <= 50.0):
        erros.append(f"ERRO: Leitura térmica inconsistente no {sensor_id} ({valor_temp}°C). Verificar hardware.")
    if not (0.0 <= valor_umid <= 100.0):
        erros.append(f"ERRO: Falha no sensor de umidade do {sensor_id} ({valor_umid}%).")
    if not (0.0 <= nh3_ppm <= 100.0):
        erros.append(f"ERRO: Leitura fora de escala para NH3 no {sensor_id} ({nh3_ppm} ppm).")
    if not (300.0 <= co2_ppm <= 10000.0):
        erros.append(f"ERRO: Leitura fora de escala para CO2 no {sensor_id} ({co2_ppm} ppm).")

    if erros:
        return {"valido": False, "sensor_id": sensor_id, "mensagem": " | ".join(erros)}

    return {
        "valido": True,
        "sensor_id": sensor_id,
        "mensagem": f"SUCESSO: Dados do {sensor_id} validados e mapeados (Altura: 50cm).",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados": {
            "temperatura_c": round(valor_temp, 2),
            "umidade_relativa": round(valor_umid, 2),
            "nh3_ppm": round(nh3_ppm, 2),
            "co2_ppm": round(co2_ppm, 2)
        }
    }

def simular_leitura_esp32(sensor_id: str = "ESP32_Norte", cenario: str = "normal") -> dict:
    """
    Simula pacote JSON enviado via protocolo MQTT pelo microcontrolador ESP32.
    """
    if cenario == "estresse_calor":
        ta = random.uniform(31.0, 35.5)
        ur = random.uniform(70.0, 82.0)
        nh3 = random.uniform(12.0, 22.0)
        co2 = random.uniform(1800.0, 2800.0)
    elif cenario == "risco_gasoso":
        ta = random.uniform(25.0, 28.0)
        ur = random.uniform(60.0, 72.0)
        nh3 = random.uniform(21.0, 32.0)
        co2 = random.uniform(3100.0, 4200.0)
    else:
        ta = random.uniform(23.5, 27.5)
        ur = random.uniform(55.0, 68.0)
        nh3 = random.uniform(4.0, 12.0)
        co2 = random.uniform(700.0, 1500.0)

    return validar_mapeamento(sensor_id, ta, ur, nh3, co2)

if __name__ == "__main__":
    print(validar_mapeamento("ESP32_Norte", 31.5, 65.0, 10.2, 1150.0)["mensagem"])
