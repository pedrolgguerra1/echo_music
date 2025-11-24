import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPlayerSurpriseVolumePause(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_select_surprise_set_volume_and_pause(self):
        driver = self.driver

        # Passo 1: Fazer login com usuário existente
        driver.get(f"{self.base_url}/accounts/login/")
        time.sleep(1)
        username = "testuser"
        password = "testpass123"

        driver.find_element(By.NAME, "username").send_keys(username)
        time.sleep(1)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Aguardar carregamento da página inicial (campo de busca)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        time.sleep(1)

        # Passo 2: Ir direto para o player
        driver.get(f"{self.base_url}/music/player/")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "audio-player"))
        )
        time.sleep(1)

        # Passo 3: Selecionar a música "surprise" no mostruário do player
        # Procura um card de música cujo título contenha "surprise"
        surprise_card = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'music-item')]"
                    "[.//p[contains(@class, 'font-semibold') and contains(translate(., 'SURPRISE', 'surprise'), 'surprise')]]",
                )
            )
        )
        surprise_card.click()

        # A página recarrega com a música selecionada
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "audio-player"))
        )
        time.sleep(1)

        # Passo 4: Ajustar o volume para 20%
        volume_slider = driver.find_element(By.ID, "volume")
        driver.execute_script(
            "arguments[0].value = 20; arguments[0].dispatchEvent(new Event('input'));",
            volume_slider,
        )
        time.sleep(1)

        # Passo 5: Apertar pause após iniciar a reprodução
        play_button = driver.find_element(By.ID, "playBtn")

        # Garantir que a música comece a tocar primeiro
        play_button.click()
        time.sleep(1)

        # Agora apertar pause
        play_button.click()
        time.sleep(2)  # esperar 2 segundos após pausar antes de finalizar o teste


if __name__ == "__main__":
    unittest.main()

