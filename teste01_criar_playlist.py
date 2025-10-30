import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestCreatePlaylist(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_create_playlist(self):
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
        time.sleep(1)

        # Aguardar carregamento da página inicial (presença do input de busca)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "searchInput")))

        # Passo 2: Navegar para a página de criação de playlist
        driver.get(f"{self.base_url}/playlists/create/")
        time.sleep(1)

        # Passo 3: Preencher o formulário de criação de playlist
        playlist_name = "Minha Playlist de Teste"
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys(playlist_name)
        time.sleep(1)

        # Submeter o formulário
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Passo 4: Verificar se a playlist foi criada
        # Aguardar redirecionamento para a página de detalhes da playlist
        WebDriverWait(driver, 10).until(EC.url_contains("playlists/"))

        # Verificar se o nome da playlist aparece na página
        page_source = driver.page_source
        self.assertIn(playlist_name, page_source)

        # Verificar se há uma mensagem de sucesso
        self.assertIn("criada com sucesso", page_source)

if __name__ == "__main__":
    unittest.main()
