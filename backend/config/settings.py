import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR.parent / 'infra_blog_0' / '.env'

env.read_env(ENV_FILE)
DEBUG = env('DEBUG', default=False)

SECRET_KEY = env('SECRET_KEY')

HOST_NAME = env('HOST_NAME', default='http://localhost')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD')
    }
}

PASSWORD_VALIDATORS = (
    'UserAttributeSimilarityValidator',
    'MinimumLengthValidator',
    'CommonPasswordValidator',
    'NumericPasswordValidator'
)
AUTH_PASSWORD_VALIDATORS = tuple() if DEBUG else (
    {'NAME': 'django.contrib.auth.password_validation.' + validator}
    for validator in PASSWORD_VALIDATORS
)

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = f'{HOST_NAME}/static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
