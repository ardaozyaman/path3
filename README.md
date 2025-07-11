# Python Selenium Test Otomasyonu ve CI/CD Pipeline

Bu proje, Selenium ile yazılmış UI testlerini `unittest` kullanarak çalıştıran, test sonuçlarını bir PostgreSQL veritabanına kaydeden ve Jenkins ile CI/CD sürecine entegre eden bir yapı sunar. Test sonuçları Grafana üzerinden görselleştirilebilir.

## 1. Lokal Kurulum ve Çalıştırma

### Gereksinimler
*   Python 3.8+
*   PostgreSQL veritabanı

### Kurulum Adımları

1.  **Projeyi Klonlayın:**
    ```sh
    git clone https://github.com/ardaozyaman/path3.git
    cd path3
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Ortam Değişkenlerini Ayarlayın:**
    *   Proje ana dizininde `.env` adında bir dosya oluşturun.
    *   İçine PostgreSQL bağlantı bilgilerinizi aşağıdaki formatta girin:
      ```properties
      # .env dosyası
      DATABASE_URL=postgresql://KULLANICI_ADI:SIFRE@localhost:5432/VERITABANI_ADI
      ```
    *   **Not:** Belirttiğiniz veritabanının PostgreSQL'de oluşturulmuş olması gerekmektedir.

5.  **Testleri Çalıştırın:**
    *   Tüm testleri çalıştırmak ve sonuçları veritabanına kaydetmek için aşağıdaki komutu kullanın:
      ```sh
      python3 run_tests.py
      ```

## 2. Jenkins Entegrasyonu

Bu proje, bir `Jenkinsfile` içerir ve Jenkins pipeline'ı ile otomatik olarak test edilebilir.

### Jenkins Agent Gereksinimleri
Pipeline'ın çalışacağı Jenkins agent'ında aşağıdaki yazılımların kurulu olması gerekir:
*   Git
*   Python 3 ve `venv`
*   Chromium Browser
*   Chromium Driver

### Jenkins Yapılandırması

1.  **Veritabanı Kimlik Bilgisi (Credential) Oluşturma:**
    *   Jenkins'te **Manage Jenkins > Credentials > System > Global credentials**'a gidin.
    *   **Add Credentials** ile yeni bir kimlik bilgisi ekleyin:
        *   **Kind:** `Secret text`
        *   **Secret:** Veritabanı bağlantı URL'niz (`postgresql://...`)
        *   **ID:** `postgres-db-credentials` (Bu ID, `Jenkinsfile`'daki ile aynı olmalıdır).

2.  **Pipeline Projesi Oluşturma:**
    *   Jenkins'te **New Item** ile yeni bir proje oluşturun ve **Pipeline** türünü seçin.
    *   Proje yapılandırmasında **Pipeline** sekmesine gidin.
    *   **Definition** olarak **Pipeline script from SCM** seçin.
    *   **SCM** olarak **Git**'i seçin ve projenizin GitHub URL'sini girin.
    *   **Branch Specifier** olarak `*/main` belirtin.
    *   Kaydedin ve **Build Now** ile pipeline'ı çalıştırın.

### Pipeline Adımları
`Jenkinsfile` aşağıdaki adımları otomatik olarak gerçekleştirir:
1.  **Checkout:** Proje kodunu `main` dalından çeker.
2.  **Setup Environment:** Python sanal ortamını oluşturur ve `requirements.txt` dosyasındaki bağımlılıkları kurar.
3.  **Run Tests:** `run_tests.py` betiğini çalıştırarak tüm testleri koşar. Test sonuçları veritabanına kaydedilir. Testlerden herhangi biri başarısız olursa pipeline da başarısız olur.

## 3. Grafana ile Sonuçları Görselleştirme

Test sonuçlarını dinamik olarak takip etmek için Grafana'yı kullanabilirsiniz.

1.  **Veri Kaynağı Ekleme:** Grafana'da yeni bir **PostgreSQL** veri kaynağı oluşturun ve `.env` dosyanızdaki bilgilerle veritabanınıza bağlayın.
2.  **Dashboard Oluşturma:** Yeni bir dashboard oluşturup paneller ekleyin.
3.  **Örnek Panel Sorguları:**
    *   **Test Süreleri (Time series):**
        ```sql
        SELECT "timestamp" AS "time", duration, test_name FROM test_results ORDER BY 1;
        ```
    *   **Başarı Oranı (Pie Chart):**
        ```sql
        SELECT status, count(*) FROM test_results GROUP BY status;
        ```

## 4. Sık Karşılaşılan Sorunlar ve Çözümleri

-   **`ImportError: cannot import name 'init_db'`:** `init_db` fonksiyonu `database.py` içinde, `insert_test_result` ise `db_operations.py` içinde olmalıdır. `import` ifadelerinin doğru dosyayı işaret ettiğinden emin olun.
-   **Jenkins'te `master` dalı bulunamadı hatası:** `Jenkinsfile` içindeki `git` adımına `branch: 'main'` parametresini ekleyin.
-   **Jenkins'te `WebDriverException` veya `NoSuchDriverException`:** Bu hata, Jenkins agent'ında tarayıcı veya sürücünün kurulu olmamasından kaynaklanır. `test_*.py` dosyalarındaki `setUp` metotları, `chromium-browser` ve `chromedriver`'ı standart Linux yollarında arayacak şekilde yapılandırılmıştır. Agent'ınızda bu yazılımların kurulu olduğundan emin olun.
