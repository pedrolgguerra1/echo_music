import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAddMusicToPlaylistBeforePlayer(unittest.TestCase):
    def setUp(self):
        # Configurar o driver do Selenium (usando Chrome)
        self.driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está instalado
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"  # URL base do servidor Django

    def tearDown(self):
        self.driver.quit()

    def test_add_music_to_playlist_then_open_player(self):
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

        # Passo 2: Escolher uma música na home e abrir o modal de playlists
        music_cards = driver.find_elements(By.CLASS_NAME, "music-card")
        self.assertGreater(
            len(music_cards),
            0,
            "Nenhuma música disponível na home para adicionar à playlist",
        )

        first_card = music_cards[0]
        add_to_playlist_btn = first_card.find_element(
            By.XPATH, ".//button[contains(., 'Adicionar à Playlist')]"
        )
        add_to_playlist_btn.click()
        time.sleep(1)

        # Modal de seleção de playlist
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "playlistModal"))
        )
        playlist_buttons = driver.find_elements(
            By.CSS_SELECTOR, "#playlistList .btn"
        )
        self.assertGreater(
            len(playlist_buttons),
            0,
            "Nenhuma playlist disponível para adicionar a música",
        )

        # Selecionar a primeira playlist
        playlist_buttons[0].click()
        time.sleep(1)

        # Confirmar alerta de sucesso
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            self.assertIn("adicionada à playlist", alert_text)
        except Exception as exc:  # noqa: BLE001
            self.fail(f"Nenhum alerta de confirmação ao adicionar música: {exc}")

        # Passo 3: Ir para o player
        player_button = driver.find_element(
            By.XPATH, "//button[contains(., 'Ir ao Player')]"
        )
        player_button.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.url_contains("/music/player")
        )
        self.assertIn("player", driver.current_url)

        # Verificar se o elemento do player de áudio está presente
        audio_elements = driver.find_elements(By.ID, "audio-player")
        self.assertGreater(
            len(audio_elements), 0, "Player de áudio não encontrado na página"
        )


if __name__ == "__main__":
    unittest.main()

