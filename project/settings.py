"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
#from dotenv import load_dotenv 
import os
# Load environment variables from .env file
#load_dotenv()
AUTH_USER_MODEL = 'app.Admin'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1_jrv9+7#usu$u!q$280jctx-e&slzyqf1ty&imx8@ww(#8o39"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
    'Authorization',
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'corsheaders',
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'app',
    'rest_framework',
    'rest_framework_simplejwt',
    #'scm_app1',
    'scm_app',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'vetrina',
#          'USER': 'root',
#          'PASSWORD': 'Root@1234', 
#          'HOST': 'localhost',
#          'PORT': '3306',
#      }
#  }
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'vetrina_ascm',
         'USER': 'dbmasteruser',
         'PASSWORD': '`9N4B8zPR7~MBp}Wo:]s+SJhO{muEJsu',
         'HOST': 'ls-161b42c3589325d6c564a0757cc05a04781e40f1.cs5wcbztw6m2.ap-south-1.rds.amazonaws.com',
         'PORT': '3306',
     }
 }


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000","http://localhost:3001","http://localhost:3002","http://localhost:3003","http://localhost:3004",
#     "http://localhost:3005"
# ]
# CORS_ALLOWED_ALL_ORIGINS = True
#DATABASES = {
 #   'default': {
  #      'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
   #     'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
    #    'USER': os.getenv('DB_USER', ''),
     #   'PASSWORD': os.getenv('DB_PASSWORD', ''),
      #  'HOST': os.getenv('DB_HOST', 'localhost'),
       # 'PORT': os.getenv('DB_PORT', ''),
    #}
#}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# settings.py
AUTHENTICATION_BACKENDS = ['app.authentication.CustomAdminBackend','app.authentication.CustomCustomerBackend',]




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
#     # Set to True if you want to rotate refresh tokens on each login
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     # 'USER_ID_FIELD': 'admin_id',
#     'USER_ID_FIELD': 'admin_id',
# }
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'USER_ID_FIELD': 'admin_id',
    'ALGORITHM': 'HS256',
}

# AUTH_USER_MODEL = 'app.Admin'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vetrina326@gmail.com'
EMAIL_HOST_PASSWORD = 'wpfd aipj pmin qepb'