import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSearchMusic(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_search_music(self):
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

        # Passo 2: Pesquisar por uma música que exista no catálogo
        # Usamos "OI NEGO", que está cadastrada via importação local
        search_query = "OI NEGO"
        search_input = driver.find_element(By.ID, "searchInput")
        search_input.clear()
        time.sleep(1)
        search_input.send_keys(search_query)
        time.sleep(3)
        # O formulário é submetido automaticamente após 500ms pelo JS da página,
        # então não precisamos enviar ENTER manualmente (evita elemento "stale").

        # Passo 3: Verificar se os resultados da busca aparecem
        # Aguardar que a página recarregue com os resultados
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "music-grid")))

        # Verificar se o termo de busca aparece na página
        page_source = driver.page_source
        self.assertIn(search_query, page_source)

        # Verificar se há músicas exibidas (pelo menos uma música na grid)
        music_cards = driver.find_elements(By.CLASS_NAME, "music-card")
        self.assertGreater(len(music_cards), 0, "Nenhuma música encontrada nos resultados da busca")

if __name__ == "__main__":
    unittest.main()
