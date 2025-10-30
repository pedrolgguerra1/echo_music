import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TestAddMusic(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_add_music(self):
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

        # Aguardar carregamento da página inicial
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "searchInput")))

        # Passo 2: Navegar para a página de upload de música
        driver.get(f"{self.base_url}/music/upload/")
        time.sleep(1)

        # Passo 3: Preencher o formulário de upload
        # Título
        title_field = driver.find_element(By.ID, "title")
        title_field.send_keys("Test Music Title")
        time.sleep(2)

        # Artista (selecionar o primeiro disponível)
        artist_select = driver.find_element(By.ID, "artist")
        options = artist_select.find_elements(By.TAG_NAME, "option")
        if len(options) > 1:  # Primeiro é "Selecione um artista"
            options[1].click()  # Selecionar o primeiro artista
        time.sleep(2)

        # Duração
        duration_field = driver.find_element(By.ID, "duration")
        duration_field.send_keys("3:45")
        time.sleep(2)

        # Arquivo de música (upload de arquivo)
        file_input = driver.find_element(By.ID, "file_url")
        # Assumir um arquivo de teste existe; substitua pelo caminho real se necessário
        test_file_path = os.path.join(os.getcwd(), "test_music.mp3")  # Criar um arquivo dummy se não existir
        if not os.path.exists(test_file_path):
            # Criar um arquivo dummy para teste
            with open(test_file_path, "wb") as f:
                f.write(b"dummy audio content")  # Conteúdo dummy
        file_input.send_keys(test_file_path)
        time.sleep(1)

        # Submeter o formulário
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(1)

        # Passo 4: Verificar se o upload foi bem-sucedido
        # Aguardar redirecionamento para o player
        WebDriverWait(driver, 10).until(EC.url_contains("player"))
        self.assertIn("player", driver.current_url)  # Verificar se redirecionou para player

if __name__ == "__main__":
    unittest.main()
