import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_operations import insert_test_result

class SearchTest(unittest.TestCase):
    def setUp(self):
        # Chrome/Chromium için headless ve diğer Jenkins ayarları
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Jenkins agent'ındaki Chromium tarayıcısının yolunu belirt
        # Eğer bu yolda değilse, agent'taki doğru yolu yazmalısınız.
        if os.path.exists('/usr/bin/chromium-browser'):
            options.binary_location = '/usr/bin/chromium-browser'
        elif os.path.exists('/usr/bin/chromium'):
            options.binary_location = '/usr/bin/chromium'

        # Jenkins agent'ındaki ChromeDriver'ın olası yollarını bul
        chromedriver_path = None
        possible_paths = ['/usr/lib/chromium/chromedriver', '/usr/bin/chromedriver', '/usr/lib/chromium-browser/chromedriver']
        for path in possible_paths:
            if os.path.exists(path):
                chromedriver_path = path
                break
        
        if not chromedriver_path:
            raise RuntimeError('ChromeDriver sistemde bulunamadı. Lütfen Jenkins agentını kontrol edin.')

        # WebDriver'ı, bulunan sürücü yolu ve seçeneklerle başlat
        service = Service(executable_path=chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def test_search_in_duckduckgo(self):
        start_time = time.time()
        status = 'fail'
        try:
            self.driver.get("https://duckduckgo.com/")
            
            # Arama kutusunu bul ve arama yap
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys("selenium")
            search_box.submit()
            
            # Sonuçların yüklenmesini bekle
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="result-title-a"]'))
            )
            
            # Sonuçların en az birinin "selenium" içerdiğini doğrula
            results = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="result-title-a"]')
            self.assertTrue(
                any("selenium" in result.text.lower() for result in results),
                "Arama sonuçları 'selenium' içermiyor."
            )
            
            status = 'pass'
        finally:
            duration = time.time() - start_time
            # test.id() yerine test metodunun adını doğrudan verelim
            insert_test_result('test_search_in_duckduckgo', status, duration)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
