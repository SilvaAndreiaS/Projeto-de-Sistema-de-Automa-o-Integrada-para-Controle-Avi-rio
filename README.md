


# Projeto de Pós-Graduação UFMT – Automação Híbrida em Aviário

Projeto de pós-graduação da **Universidade Federal de Mato Grosso (UFMT)** voltado ao desenvolvimento de uma **solução de automação híbrida aplicada a aviários**, integrando sistemas de **controle**, **monitoramento ambiental** e **análise de dados zootécnicos**.

---

## 🎯 Objetivo do Projeto

Desenvolver e validar uma arquitetura de automação híbrida capaz de:
- Monitorar variáveis ambientais em tempo real
- Controlar automaticamente o microclima do aviário
- Reduzir estresse térmico e mortalidade das aves
- Apoiar a tomada de decisão por meio da análise de dados

---

## 🧪 Metodologia

O sistema foi desenvolvido com base nos princípios da **avicultura de precisão**, utilizando sensores ambientais instalados na zona de respiração das aves (≈ 50 cm do piso).

A validação ocorreu por meio da comparação entre:
- **Grupo Experimental (GE)**: aviário com automação híbrida
- **Grupo Controle (GC)**: manejo convencional

---

## 📊 Métricas Avaliadas

- **Ganho de Peso Médio (GPM)**
- **Conversão Alimentar (CA)**
- **Taxa de Mortalidade**
- **Concentração de Amônia (NH₃)**

Essas métricas permitiram avaliar o impacto do controle ambiental no desempenho zootécnico.

---

## 🏗️ Dimensionamento do Aviário

| Parâmetro | Especificação |
|---------|---------------|
| Dimensões | 12 m × 30 m |
| Área total | 360 m² |
| Densidade | 10 a 11 aves/m² |
| Capacidade | ~4.000 aves |
| Ciclo produtivo | 65 a 75 dias |
| Pé-direito | ≥ 2,80 m |

---

## 🧠 Arquitetura do Sistema

- Sensoriamento ambiental (temperatura, umidade, NH₃)
- Processamento de dados em Python
- Controle automático de ventilação
- Armazenamento de dados históricos
- Análise para suporte à decisão

---

## 💻 Exemplo de Código (Python)

```python
import time
from sensors import read_temperature, read_humidity, read_ammonia
from actuators import control_ventilation

TEMP_MAX = 28.0
NH3_MAX = 20  # ppm

while True:
    temp = read_temperature()
    hum = read_humidity()
    nh3 = read_ammonia()

    print(f"Temp: {temp}°C | UR: {hum}% | NH3: {nh3} ppm")

    if temp > TEMP_MAX or nh3 > NH3_MAX:
        control_ventilation("ON")
    else:
        control_ventilation("OFF")

    time.sleep(60)
