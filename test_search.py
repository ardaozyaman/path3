import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_operations import insert_test_result

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
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
