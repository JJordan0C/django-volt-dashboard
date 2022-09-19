import os, environ
from   unipath import Path
from django.db import models

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.home',  # Enable the inner home (home)
    'apps.quote',
    'apps.authentication.config.AuthConfig',
    
    'django_apscheduler',
    'bulk_update_or_create'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # login middleware
    'apps.authentication.middleware.AuthMiddleware',
]

LOGIN_URL = '/auth/login/'

ROOT_URLCONF = 'core.urls'
# LOGIN_REDIRECT_URL = "generate-quote"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "login"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.getenv('DB_NAME'     , 'appseed_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
        'HOST'    : os.getenv('DB_HOST'     , 'localhost'),
        'PORT'    : os.getenv('DB_PORT'     , 3306),
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'it-IT'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

# DEALER_TABLES = [
#     {
#         'name': 'QuoteTypes',
#         'fields': {
#             'id': models.AutoField(primary_key=True) ,
#             'name': models.CharField(max_length=50, blank=True ),
#         }
#     }, 
#     {
#         'name': 'Competitions',
#         'fields': {
#             'id': models.AutoField(primary_key=True) ,
#             'name': models.CharField(max_length=50),
#         }
#     },
#     {
#         'name': 'Events',
#         'fields': {
#             'id': models.AutoField(primary_key=True) ,
#             'name': models.CharField(max_length=50),
#             'competition_id': lambda x: models.ForeignKey(to=f'quote.{x}Competitions', on_delete=models.deletion.CASCADE)
#         }
#     },
#     {
#         'name': 'EventQuote',
#         'fields': {
#             'id': models.AutoField(primary_key=True) ,
#             'name': models.CharField(max_length=50),
#             'event_id': lambda x: models.ForeignKey(to=f'quote.{x}Events', on_delete=models.deletion.CASCADE),
#             'qt_id': lambda x: models.ForeignKey(to=f'quote.{x}QuoteTypes', on_delete=models.deletion.CASCADE),
#             'quote': models.FloatField()
#         }
#     }

# ] 

AUTH_USER_MODEL = 'apps_auth.User' 

DEALERS = {
    9 : 'Goldbet',
    11 : 'Snai',
    13 : 'Eurobet',
    14 : 'Planetwin',
    15 : 'Stanleybet'
}

PDF_QUOTE_TYPES = {
    9 : [
        104, 105, 106,  # ESITO FINALE 1 X 2
        191, 192, 193,  # ESITO FINALE 1° TEMPO 1 X 2
        801, 802, 803,  # DOPPIA CHANCE 1X 12 X2
        1612, 1613,     # UNDER/OVER 1,5 U O
        1622, 1623,     # UNDER/OVER 2,5 U O
        1624, 1625,     # UNDER/OVER 3,5 U O
        970, 971,       # GOAL/NOGOAL GG NG
    ],
    11 : [
        160, 161, 162,  # ESITO FINALE 1 X 2
        301, 302, 303,  # ESITO FINALE 1° TEMPO 1 X 2
        546, 547, 548,  # DOPPIA CHANCE 1X 12 X2  (DA VEDERE SE GIUSTO PERCHE' DC IN/DC OUT ???)
        1601, 1602,     # UNDER/OVER 1,5 U O
        1603, 1604,     # UNDER/OVER 2,5 U O
        1609, 1610,     # UNDER/OVER 3,5 U O
        613, 614,       # GOAL/NOGOAL GG NG
    ],
    13 : [
        159, 160, 161,  # ESITO FINALE 1 X 2
        267, 268, 269,  # ESITO FINALE 1° TEMPO 1 X 2
        99, 28, 1173,   # DOPPIA CHANCE 1X 12 X2 (NON SI TROVANO O 1X|1X 2X|2X ??)
        1042, 1043,     # UNDER/OVER 1,5 U O
        1044, 1045,     # UNDER/OVER 2,5 U O
        1046, 1047,     # UNDER/OVER 3,5 U O
        377, 378,       # GOAL/NOGOAL GG NG
    ],
    14 : [
        16, 17, 18,     # ESITO FINALE 1 X 2
        660, 661, 662,  # ESITO FINALE 1° TEMPO 1 X 2
        298, 299, 300,  # DOPPIA CHANCE 1X 12 X2
        554, 553,       # UNDER/OVER 1,5 U O
        560, 559,       # UNDER/OVER 2,5 U O
        566, 565,       # UNDER/OVER 3,5 U O
        365, 366,       # GOAL/NOGOAL GG NG
    ],
    15 : [
        1, 2, 3,        # ESITO FINALE 1 X 2
        332, 333, 334,  # ESITO FINALE 1° TEMPO 1 X 2
        104, 105, 106,  # DOPPIA CHANCE 1X 12 X2
        380, 381,       # UNDER/OVER 1,5 U O
        386, 387,       # UNDER/OVER 2,5 U O
        392, 393,       # UNDER/OVER 3,5 U O
        115, 116,       # GOAL/NOGOAL GG NG
    ],
}

           
QUOTE_URL = "http://www.tradingm3.com/failbook/Sure/suresystem/service/bvaquoteall.aspx?book={dealer_id}&sport=0"

#DJANGO APSCHEDULER
APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']