from dotenv import load_dotenv
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-vk)z_&2d=6zf7o)!7xmsys$3x8(8ug(9pi3e8z2ks)mqw$v2x0'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'chatbot',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'ChatBotAi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'ChatBotAi.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'djongo',  # Nếu dùng Djongo (bạn bảo không dùng Djongo thì đổi ENGINE phù hợp)
        'NAME': 'chatbotDB',  # Đổi thành tên database của bạn
        'CLIENT': {
            'host': 'mongodb://localhost:27017/',
        }
    }
}

print("DATABASES config:", DATABASES)  # Debug thông tin cấu hình DATABASES


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("MONGO_URI:", MONGO_URI)  # Debug xem biến môi trường có được load không


load_dotenv()  # Load biến môi trường từ file .env
print(f"API Key sau khi load: {os.getenv('GEMINI_API_KEY')}")

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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = True  # Cho phép tất cả domain truy cập API