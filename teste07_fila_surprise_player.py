import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestQueueSurpriseAndSelectInPlayer(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_queue_surprise_then_choose_second_and_back(self):
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

        # Passo 2: Na home, adicionar a música "surprise" à fila
        surprise_card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'music-card')]"
                    "[.//h3[contains(translate(., 'SURPRISE', 'surprise'), 'surprise')]]",
                )
            )
        )
        add_to_queue_btn = surprise_card.find_element(
            By.XPATH, ".//button[contains(., 'Adicionar à Fila')]"
        )
        add_to_queue_btn.click()
        time.sleep(1)

        # Confirmar alerta de adição à fila
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        self.assertIn("fila", alert_text.lower())

        # Passo 3: Entrar no player
        player_button = driver.find_element(
            By.XPATH, "//button[contains(., 'Ir ao Player')]"
        )
        player_button.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "audio-player"))
        )
        time.sleep(1)

        # Passo 4: Escolher a música 2 no mostruário (segundo item da grid)
        showcase_items = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "div.grid div.music-item")
        )
        self.assertGreaterEqual(
            len(showcase_items), 2, "Menos de duas músicas no mostruário do player"
        )
        showcase_items[1].click()  # música 2

        # A página recarrega com a música 2 selecionada
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "audio-player"))
        )
        time.sleep(1)

        # Passo 5: Selecionar "surprise" que está na fila "Em seguida"
        surprise_queue_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//h3[contains(., 'Em seguida')]/following-sibling::div"
                    "[contains(@class, 'music-item')]"
                    "[.//p[contains(@class, 'font-semibold') and "
                    "contains(translate(., 'SURPRISE', 'surprise'), 'surprise')]]",
                )
            )
        )
        surprise_queue_item.click()

        # A página recarrega novamente com surprise selecionada
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "audio-player"))
        )
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()

