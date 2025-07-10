pipeline {
    // 1. Çalışma Ortamı: Jenkins'in bu pipeline'ı herhangi bir uygun agent'ta çalıştırmasını sağlar.
    // Python ve Chrome'un bu agent'ta kurulu olması gerekir.
    agent any

    // 2. Ortam Değişkenleri: Veritabanı bağlantı bilgilerini güvenli bir şekilde yönetir.
    // 'postgres-db-credentials' Jenkins'te oluşturacağınız bir "Secret text" credential ID'sidir.
    environment {
        DATABASE_URL = credentials('postgres-db-credentials')
    }

    stages {
        // 3. Adım: Kodu Çekme
        stage('Checkout') {
            steps {
                // Hangi dalın (branch) kullanılacağını belirtiyoruz.
                git branch: 'main', url: 'https://github.com/ardaozyaman/path3.git'
            }
        }

        // 4. Adım: Bağımlılıkları Kurma
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        // 5. Adım: Testleri Çalıştırma
        stage('Run Tests') {
            steps {
                // run_tests.py betiği çalıştırılır.
                // Betik başarısız olursa (çıkış kodu 0'dan farklı olursa),
                // Jenkins bu adımı ve tüm pipeline'ı başarısız olarak işaretler.
                sh '. venv/bin/activate && python3 run_tests.py'
            }
        }
    }

    // 6. Adım: Temizlik
    // Pipeline başarılı da olsa başarısız da olsa her zaman çalışır.
    post {
        always {
            echo 'Pipeline tamamlandı.'
            // Sanal ortamı veya geçici dosyaları temizleyebilirsiniz.
            deleteDir() 
        }
    }
}