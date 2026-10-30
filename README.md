# SISTEMA DE AUTOMAÇÃO INTEGRADA PARA CONTROLE AVIÁRIO: OTIMIZAÇÃO DO ÍNDICE DE TEMPERATURA E UMIDADE GLOBAL (ITGU) E DA QUALIDADE GASOSA PARA EFICIÊNCIA PRODUTIVA NA AVICULTURA DE PRECISÃO

## Autores

**ANDREIA SOUZA S. DA SILVA**¹  
**CRISTIANO CRUZ**²  
**ELIENAI CARDOSO**³  
**KENNEDY CRUZ LEITE**⁴  
**WAGNER**⁵

¹⁻⁵ Universidade Federal de Mato Grosso (UFMT)  
**Programa de Pós-Graduação em Agrocomputação**

---

# RESUMO

A avicultura de precisão tem incorporado tecnologias digitais com o objetivo de otimizar os processos produtivos, garantir o bem-estar animal e melhorar a eficiência operacional dos sistemas de produção. Neste contexto, o presente trabalho apresenta o desenvolvimento de um sistema de automação híbrida e integrada em Python para monitoramento e controle ambiental em aviários, fundamentado em conceitos de Internet das Coisas (IoT), automação rural e análise de dados.

A solução desenvolvida permite a aquisição contínua de temperatura, umidade relativa do ar e concentração de gases (amônia - $\text{NH}_3$ e dióxido de carbono - $\text{CO}_2$), promovendo a avaliação das condições ambientais por meio do Índice de Temperatura e Umidade Global (ITGU). O sistema integra sensores, banco de dados, mecanismos automáticos de ventilação com controle adaptativo e ferramentas de visualização, possibilitando a tomada de decisão baseada em dados e a redução de custos energéticos em até 40%.

Os resultados demonstram o potencial da automação aplicada à avicultura de precisão para redução do estresse térmico, melhoria das condições de ambiência e apoio ao gerenciamento produtivo.

**Palavras-chave:** Avicultura de Precisão; Automação Rural; Internet das Coisas; ITGU; Monitoramento Ambiental; Qualidade Gasosa.

---

# 1. INTRODUÇÃO

A produção avícola moderna depende diretamente do controle das condições ambientais para garantir elevados índices de desempenho produtivo e zootécnico. Embora o melhoramento genético tenha tornado o Brasil uma liderança mundial no setor, a evolução metabólica tornou as aves homeotérmicas extremamente sensíveis às oscilações ambientais, fazendo com que o monitoramento tradicional apenas por temperatura de bulbo seco seja insuficiente. Estima-se que o estresse térmico em regiões semiáridas cause perdas econômicas na ordem de R$ 2 bilhões anuais.

O uso de tecnologias de automação associadas à Internet das Coisas (IoT) permite o monitoramento contínuo de temperatura, umidade e gases ($\text{NH}_3$ e $\text{CO}_2$), fornecendo informações em tempo real e possibilitando respostas automáticas e preditivas às alterações ambientais. Dessa forma, a automação integrada representa uma alternativa indispensável para aumentar a eficiência energética e produtiva dos sistemas de criação e contribuir para a sustentabilidade e o bem-estar animal.

---

# 2. OBJETIVOS

## 2.1 Objetivo Geral

Desenvolver um sistema de automação híbrida integrada em Python para monitoramento e controle ambiental adaptativo aplicado à produção avícola.

## 2.2 Objetivos Específicos

- Monitorar continuamente temperatura, umidade relativa do ar e concentração de amônia ($\text{NH}_3$) e gás carbônico ($\text{CO}_2$) via sensores IoT;
- Calcular e otimizar indicadores ambientais em tempo real, com foco no ITGU;
- Armazenar dados históricos em banco de dados;
- Automatizar o acionamento de exaustores, nebulizadores e cortinas com controle adaptativo de velocidade do ar;
- Reduzir custos energéticos em até 40% através do controle inteligente;
- Disponibilizar gráficos e relatórios técnicos para apoiar a tomada de decisão;
- Avaliar indicadores ambientais e zootécnicos (Ganho de Peso Médio, Conversão Alimentar e Taxa de Mortalidade).

---

# 3. MATERIAL E MÉTODOS

## 3.1 Caracterização da Unidade Experimental

| Parâmetro | Valor |
|------------|---------|
| Comprimento | 30 m |
| Largura | 12 m |
| Área Total | 360 m² |
| Capacidade Instalada | Aproximadamente 4.000 aves |
| Densidade de Alojamento | 10 a 11 aves/m² |
| Ciclo Produtivo | 65 a 75 dias |
| Pé-direito | ≥ 2,80 m |

## 3.2 Delineamento Experimental

### Grupo Experimental (GE)

Aviário equipado com sistema de automação híbrida integrada em Python para monitoramento e controle ambiental preditivo e adaptativo.

### Grupo Controle (GC)

Aviário submetido ao manejo convencional, sem utilização da automação desenvolvida.

## 3.3 Variáveis e Métricas Monitoradas

- Temperatura do ar (°C) e Umidade relativa do ar (%);
- Concentração de amônia ($\text{NH}_3$ em ppm) e dióxido de carbono ($\text{CO}_2$);
- Estado dos atuadores (exaustores, nebulizadores e cortinas) e consumo energético (kWh);
- Índice de Temperatura e Umidade Global (ITGU);
- Métricas Zootécnicas: Ganho de Peso Médio (GPM), Conversão Alimentar (CA) e Taxa de Mortalidade.

---

# 4. ARQUITETURA DO SISTEMA

A arquitetura IoT e de software do sistema foi estruturada nos seguintes componentes e módulos:

1. **Gateway Central (Raspberry Pi):** Execução da lógica central em Python, processamento de dados em tempo real e tomada de decisão baseada em algoritmos adaptativos de ITGU;
2. **Microcontroladores (ESP32 / Arduino):** Interface de atuação física via módulos de relés e comunicação sem fio estável para controle de exaustores, nebulizadores e cortinas;
3. **Lógica Híbrida Preditiva:** Antecipação de riscos sanitários monitorando o acúmulo de gases ($\text{NH}_3$/$\text{CO}_2$) antes que atinjam níveis críticos;
4. **Módulos de Software:** Sensoriamento Ambiental, Aquisição de Dados, Processamento, Banco de Dados, Controle Automático, Exportação (CSV), Visualização e Geração de Relatórios.

---

# 5. FLUXO OPERACIONAL

```mermaid
flowchart TD

A[Início] --> B[Leitura dos Sensores]
B --> C[Validação das Leituras]
C --> D{Leituras Válidas?}
D -->|Não| E[Registrar Falha]
E --> F[Executar Contingência]
F --> B
D -->|Sim| G[Salvar Dados]
G --> H[Avaliar Limites Ambientais e ITGU]
H --> I{Necessita Intervenção?}
I -->|Não| J[Continuar Monitoramento]
J --> B
I -->|Sim| K[Acionar Ventilação / Nebulização]
K --> L[Registrar Evento]
L --> B
