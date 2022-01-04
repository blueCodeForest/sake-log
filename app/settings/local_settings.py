import os
print('local_settings')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# django-debug-toolbarの設定
INTERNAL_IPS = ['127.0.0.1']

# django-debug-toolbarの設定
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : lambda request: True,
}

ALLOWED_HOSTS = []

DEBUG = True
