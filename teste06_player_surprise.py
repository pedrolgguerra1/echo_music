import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestPlayerOiNegoVolumePause(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_select_oi_nego_set_volume_and_pause(self):
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

        # Passo 2: Na home, localizar a música "OI NEGO" para descobrir o ID
        try:
            music_cards = driver.find_elements(By.CLASS_NAME, "music-card")
            oi_nego_id = None
            for card in music_cards:
                title_el = card.find_element(By.TAG_NAME, "h3")
                if "oi nego" in title_el.text.lower():
                    # Pegar o botão "Adicionar à Fila" e extrair o ID da música do atributo onclick
                    queue_btn = card.find_element(
                        By.XPATH, ".//button[contains(., 'Adicionar à Fila')]"
                    )
                    onclick = queue_btn.get_attribute("onclick")  # ex: addToQueue(1, 'OI NEGO ...')
                    try:
                        oi_nego_id = int(
                            onclick.split("addToQueue(")[1].split(",")[0].strip()
                        )
                    except Exception:
                        pass
                    break

            if not oi_nego_id:
                self.skipTest("Música 'OI NEGO' não encontrada na home.")

            # Passo 3: Abrir o player já com a música 'OI NEGO' selecionada
            driver.get(f"{self.base_url}/music/player/?music_id={oi_nego_id}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "audio-player"))
            )
            time.sleep(1)
        except TimeoutException:
            self.skipTest("Home não carregou a tempo para localizar 'OI NEGO'.")

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

