"""
Suíte de Testes Unitários e Validação de Hardware/Software - Aviário Inteligente UFMT
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
from calculo_itgu import calcular_temperatura_ponto_orvalho, calcular_itgu, classificar_conforto_termico
from sensores import validar_mapeamento
from controle_automatico import ControladorHibridoAviario

class TestAutomacaoAviaria(unittest.TestCase):
    def test_validacao_sensor_esp32_norte_sucesso(self):
        res = validar_mapeamento("ESP32_Norte", 31.5, 65.0, 10.0, 1100.0)
        self.assertTrue(res["valido"])
        self.assertIn("SUCESSO", res["mensagem"])

    def test_validacao_sensor_temperatura_invalida(self):
        res = validar_mapeamento("ESP32_Sul", 65.0, 50.0)
        self.assertFalse(res["valido"])
        self.assertIn("ERRO", res["mensagem"])

    def test_calculo_itgu_precisao(self):
        tpo = calcular_temperatura_ponto_orvalho(30.0, 70.0)
        itgu = calcular_itgu(31.5, tpo)
        self.assertGreater(itgu, 75.0)
        avaliacao = classificar_conforto_termico(itgu, semana_vida=6)
        self.assertEqual(avaliacao["status"], "ESTRESSE_CALORICO_CRITICO")

    def test_prioridade_emergencia_gasosa(self):
        ctrl = ControladorHibridoAviario(itgu_setpoint=72.0)
        # Mesmo com ITGU ameno (70.0), se NH3 passar de 20 ppm deve acionar exaustão de emergência
        atuacao = ctrl.calcular_atuacao(itgu_atual=70.0, ur_atual=60.0, nh3_ppm=24.5, co2_ppm=1500.0)
        self.assertTrue(atuacao["alerta_gases"])
        self.assertEqual(atuacao["modo_operacao"], "EMERGENCIA_SANITARIA_GASES")
        self.assertGreaterEqual(atuacao["potencia_exaustores_pct"], 85.0)

if __name__ == "__main__":
    unittest.main()
