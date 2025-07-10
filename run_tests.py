import unittest
import time
import sys
from db_operations import insert_test_result
from database import init_db

class DatabaseTestResult(unittest.TextTestResult):
    """
    unittest sonuçlarını yakalayıp veritabanına kaydeden özel TestResult sınıfı.
    """
    def startTest(self, test):
        self.start_time = time.time()
        super().startTest(test)
        print(f"Running test: {test.id()} ... ", end="")

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time.time() - self.start_time
        insert_test_result(test.id(), 'pass', duration)
        print("PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        duration = time.time() - self.start_time
        insert_test_result(test.id(), 'fail', duration)
        print("FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        duration = time.time() - self.start_time
        # Hataları da 'fail' olarak kaydediyoruz.
        insert_test_result(test.id(), 'fail', duration)
        print("ERROR")

if __name__ == "__main__":
    # Veritabanı ve tabloyu başlat/kontrol et
    init_db()

    # Proje dizinindeki 'test_' ile başlayan tüm testleri bul
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')

    # Özel TestResult sınıfımızı kullanan bir runner oluştur
    runner = unittest.TextTestRunner(resultclass=DatabaseTestResult)
    
    # Testleri çalıştır
    result = runner.run(suite)

    # Jenkins'in pipeline durumunu belirlemesi için çıkış kodu ayarla
    # Eğer herhangi bir test başarısız olduysa veya hata verdiyse, çıkış kodu 1 olacak.
    if not result.wasSuccessful():
        sys.exit(1)
