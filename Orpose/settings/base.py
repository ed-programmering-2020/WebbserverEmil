import os


SECRET_KEY = 'u2v4es^aj+c4d5g_@eh!!st@d8w6kpfz0^^evta15n@**lmc0r'
ROOT_URLCONF = 'Orpose.urls'
WSGI_APPLICATION = 'Orpose.wsgi.application'

# Static
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = '/static/'
STATIC_FILES = []

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

# Authentication
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
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
CORS_ORIGIN_WHITELIST = [
    "https://www.orpose.se",
    "https://orpose.se",
    "http://localhost:3000"
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

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
