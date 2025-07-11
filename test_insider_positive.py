import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class InsiderCareersTest(unittest.TestCase):
    driver = None  # Sınıf seviyesinde driver tanımı
    "test commit"

    @classmethod
    def setUpClass(cls):
        # Tarayıcıyı sadece bir kez, tüm testler başlamadan önce başlat
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Jenkins agent'ındaki Chromium tarayıcısının yolunu belirt
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

        service = Service(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=service, options=options)
        os.makedirs('reports/screenshots', exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Tüm testler bittikten sonra tarayıcıyı kapat
        if cls.driver:
            cls.driver.quit()

    def test_find_dream_job_button(self):
        self.driver.get("https://useinsider.com/careers/")
        
        # Butonun görünür olmasını bekle (en fazla 10 saniye)
        try:
            button_xpath = '//a[contains(text(), "Find your dream job")]'
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
        except Exception as e:
            self.fail(f"Buton 10 saniye içinde bulunamadı: {e}")

        # Ekran görüntüsü al
        self.driver.save_screenshot('reports/screenshots/find_dream_job.png')
        
        # Elementin varlığını doğrula
        elements = self.driver.find_elements(By.XPATH, button_xpath)
        self.assertTrue(len(elements) > 0, 'Find your dream job butonu bulunamadı!')

if __name__ == "__main__":
    unittest.main()
