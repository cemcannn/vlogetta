# 🚀 Render.com Deployment Rehberi

## 📋 Ön Hazırlık

### 1. GitHub Repository'yi Hazırla
```bash
git add .
git commit -m "🚀 Render.com deployment ayarları"
git push origin main
```

### 2. Render.com'da Hesap Oluştur
- [render.com](https://render.com) adresinden ücretsiz hesap oluştur
- GitHub hesabını bağla

## 🔧 Deployment Adımları

### 1. Render Dashboard'da Yeni Servis
1. **"New +"** butonuna tıkla
2. **"Web Service"** seç
3. GitHub repository'yi bağla: `cemcannn/vlogetta`
4. Branch: `main`

### 2. Servis Ayarları
```
Name: vlogetta-web
Environment: Python
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn vlogetta.wsgi:application
```

### 3. Environment Variables (Ortam Değişkenleri)
Dashboard'da Environment bölümüne ekle:

```bash
SECRET_KEY=p=bcv=722#inpg3^y2ma(yz!%!k_fiyduwjfkzckq$kck3r7rx
DEBUG=False
RENDER=True
ALLOWED_HOSTS=*
```

### 4. PostgreSQL Veritabanı
1. **"New +"** → **"PostgreSQL"** seç
2. Name: `vlogetta-db`
3. Plan: **Free**
4. Veritabanı oluşturulduktan sonra `DATABASE_URL`'i kopyala
5. Web servisine `DATABASE_URL` environment variable olarak ekle

### 5. Kalıcı Disk (Media Files)
1. Web servis ayarlarında **"Disks"** bölümü
2. **"Add Disk"** tıkla
3. Name: `media-storage`
4. Mount Path: `/app/media`
5. Size: `1 GB` (Free plan)

## 🎯 Otomatik Deployment (render.yaml)

Repository'de `render.yaml` dosyası mevcut. Bu dosya sayesinde:
- Otomatik deployment yapılandırması
- PostgreSQL veritabanı otomatik oluşturma
- Environment variables otomatik set etme

**Deploy etmek için:**
1. Render Dashboard'da **"New +"** 
2. **"Blueprint"** seç
3. Repository'yi seç
4. `render.yaml` dosyasını otomatik algılayacak

## 📱 İlk Deployment Sonrası

### 1. Superuser Oluştur
Render Dashboard → Web Service → Shell açarak:
```bash
python manage.py createsuperuser
```

### 2. Test Et
- Site URL'ine git
- Admin paneli: `your-app.onrender.com/admin`
- Blog sayfası: `your-app.onrender.com/blog`

### 3. Domain Ayarları
- Custom domain eklemek için Render Pro plan gerekli
- Free plan: `your-app-name.onrender.com` URL'i

## 🔒 Güvenlik Notları

### Production SECRET_KEY
```python
# Güçlü SECRET_KEY oluştur:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Environment Variables
- `DEBUG=False` (Production)
- `ALLOWED_HOSTS` domain adresini içermeli
- `SECRET_KEY` production için değiştirilmeli

## 🆘 Sorun Giderme

### Common Issues:
1. **Static files yüklenmiyor** → WhiteNoise middleware eklendi ✅
2. **Media files kaybolyor** → Persistent disk yapılandırıldı ✅
3. **Database connection error** → DATABASE_URL kontrol et
4. **Build fails** → requirements.txt kontrol et

### Logs Kontrol:
Render Dashboard → Service → Logs

## 🎉 Deployment Tamamlandı!

Site URL: `https://your-app-name.onrender.com`
Admin: `https://your-app-name.onrender.com/admin`

Free plan limitasyonları:
- 750 saat/ay ücretsiz
- Site 15dk inaktiflikten sonra uyur
- İlk request yavaş olabilir (cold start)
