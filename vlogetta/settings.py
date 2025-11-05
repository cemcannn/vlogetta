"""
Django settings for vlogetta project.
...
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# .env dosyasını yükle
load_dotenv(BASE_DIR.parent / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECRET_KEY kontrolü - eğer .env dosyasında yoksa hata ver
if not SECRET_KEY:
    raise ValueError("SECRET_KEY ortam değişkeni tanımlanmamış! .env dosyasını kontrol edin.")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG ayarını ortam değişkeninden okuyun. Canlı ortamda 'False' olmalıdır.
DEBUG = os.environ.get('DEBUG', 'True') == 'True' # Varsayılan olarak geliştirmedeki gibi 'True'

# ALLOWED_HOSTS'u ortam değişkeninden okuyun.
# Canlı ortamda 'www.siteadi.com,siteadi.com' gibi bir değer verilmelidir.
allowed_hosts_str = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = []
if allowed_hosts_str:
    ALLOWED_HOSTS = allowed_hosts_str.split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vlogetta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vlogetta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# PostgreSQL veritabanı ayarları
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'vlogetta_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'tr-tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I1N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# STATIC_ROOT ayarını ekleyin. Canlı ortamda (production) 'collectstatic' komutu
# tüm statik dosyaları bu klasörde toplayacaktır.
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'