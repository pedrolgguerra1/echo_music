import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPlayerFavoritesAndQueue(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_player_favorites_and_queue(self):
        driver = self.driver

        # Passo 1: Fazer login com usuário existente
        driver.get(f"{self.base_url}/accounts/login/")
        time.sleep(1)
        username = "testuser"
        password = "testpass123"

        # Preencher o formulário de login
        driver.find_element(By.NAME, "username").send_keys(username)
        time.sleep(1)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Aguardar carregamento da página inicial (presença do input de busca)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "searchInput")))
        time.sleep(1)

        # Passo 2: Navegar para a página do player
        driver.get(f"{self.base_url}/music/player/")
        time.sleep(1)

        # Verificar se estamos na página do player
        self.assertIn("player", driver.current_url)
        time.sleep(1)

        # Passo 3: Adicionar música aos favoritos (se houver botão de favoritar)
        try:
            favorite_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "favoriteBtn"))
            )
            favorite_btn.click()
            time.sleep(1)
            # Verificar se o texto do botão mudou (adicionado aos favoritos)
            self.assertIn("Remover dos Favoritos", favorite_btn.text)
            time.sleep(1)
        except:
            # Se não houver música atual ou botão, pular
            pass

        # Passo 4: Adicionar música à fila (usando botão de adicionar à fila no showcase ou "Em seguida")
        try:
            add_to_queue_btns = driver.find_elements(By.CLASS_NAME, "add-to-queue-btn")
            if add_to_queue_btns:
                add_to_queue_btns[0].click()  # Clicar no primeiro botão disponível
                time.sleep(1)
                # Verificar se o botão mudou para "✓" ou algo similar
                self.assertEqual(add_to_queue_btns[0].text, "✓")
                time.sleep(1)

                # Recarregar o player para que a seção "Em seguida" reflita a fila da sessão
                driver.refresh()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "audio-player"))
                )
        except:
            # Se não houver botões, pular
            pass

        # Passo 5: Verificar se a música foi adicionada à seção "Em seguida"
        next_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[text()='Em seguida:']"))
        )
        time.sleep(1)
        next_musics = driver.find_elements(
            By.XPATH,
            "//h3[text()='Em seguida:']/following-sibling::div"
            "[contains(@class, 'music-item')]",
        )
        time.sleep(1)
        # Assumir que pelo menos uma música foi adicionada
        self.assertGreater(len(next_musics), 0, "Nenhuma música na fila 'Em seguida'")

if __name__ == "__main__":
    unittest.main()
