import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_KEY = 'u2v4es^aj+c4d5g_@eh!!st@d8w6kpfz0^^evta15n@**lmc0r'

# React config
REACT_APP_DIR = "/home/Orpose/Orpose-Frontend/"
REACT_BUILD_DIR = os.path.join(REACT_APP_DIR, 'build')

# Static config
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_ROOT,
    REACT_BUILD_DIR
]

INSTALLED_APPS = [
    # Third Part apps
    "corsheaders",
    "rest_framework",
    "knox",
    "admin_reorder",

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    "users",
    "products",
    "content",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

# Rest setup
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

ROOT_URLCONF = 'Orpose.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, "static")],
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

WSGI_APPLICATION = 'Orpose.wsgi.application'

# Authentication
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ('users.backends.MyAuthBackend', 'django.contrib.auth.backends.ModelBackend',)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Administration
ADMIN_REORDER = (
    {
        "app": "products",
        "label": "Products (Products)",
        "models": (
            "products.Laptop",
            "products.MetaProduct",
            "products.Website",
        ),
    }, {
        "app": "products",
        "label": "Specifications (Products)",
        "models": (
            "products.Processor",
            "products.GraphicsCard",
            "products.PanelType",
            "products.RefreshRate",
            "products.Resolution",
            "products.ScreenSize",
            "products.Ram",
            "products.StorageSize",
            "products.StorageType",
            "products.BatteryTime",
            "products.Weight",
            "products.Height"
        )
    },
    "users",
    "content",
    "contenttypes",
    "knox"
)

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


