# Vlogetta

Vlogetta, Django framework kullanılarak geliştirilmiş modern bir blog ve vlog platformudur.

## Özellikler

- Modern ve responsive tasarım
- Blog yazıları yönetimi
- Kategori sistemi
- Medya dosyaları desteği
- Admin paneli
- Kullanıcı dostu arayüz

## Teknolojiler

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Veritabanı**: SQLite
- **Static Files**: Bootstrap, AOS, jQuery

## Kurulum

### Gereksinimler

- Python 3.8+
- pip

### Adımlar

1. Repository'yi klonlayın:
```bash
git clone https://github.com/[kullaniciadi]/vlogetta.git
cd vlogetta
```

2. Virtual environment oluşturun ve aktifleştirin:
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
# veya
env\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Ortam değişkenlerini ayarlayın:
```bash
# .env.example dosyasını .env olarak kopyalayın
cp .env.example .env

# .env dosyasını düzenleyerek SECRET_KEY ve diğer ayarları yapın
# SECRET_KEY için güvenli bir anahtar üretmek için:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Veritabanı migration'larını çalıştırın:
```bash
python manage.py migrate
```

6. Süper kullanıcı oluşturun (isteğe bağlı):
```bash
python manage.py createsuperuser
```

7. Sunucuyu başlatın:
```bash
python manage.py runserver
```

8. Tarayıcınızda `http://127.0.0.1:8000` adresine gidin.

## Proje Yapısı

```
vlogetta/
├── blog/                 # Blog uygulaması
├── pages/               # Sayfa uygulaması  
├── static/              # Static dosyalar (CSS, JS, resimler)
├── templates/           # HTML şablonları
├── media/               # Kullanıcı yüklenen dosyalar
├── vlogetta/           # Ana proje ayarları
└── manage.py           # Django yönetim scripti
```

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Proje sahibi: Cem Can
Email: cmcan@windowslive.com

Proje Linki: [https://github.com/cemcan/vlogetta](https://github.com/cemcan/vlogetta)
