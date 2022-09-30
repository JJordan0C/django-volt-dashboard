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
    'bulk_update_or_create',
    "phonenumber_field"
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
            '1X2|1', '1X2|X', '1X2|2',
            '1X2 1T|1', '1X2 1T|X', '1X2 1T|2',
            'DC|1X', 'DC|12', 'DC|X2',
            'U/O 1.5|U', 'U/O 1.5|O',
            'U/O 2.5|U', 'U/O 2.5|O',
            'U/O 3.5|U', 'U/O 3.5|O',
            'GG/NG|GG', 'GG/NG|NG',
        ],
    11 : [
        '1X2 FINALE|1', '1X2 FINALE|X', '1X2 FINALE|2',  
        '1X2 TEMPO 1|1', '1X2 TEMPO 1|X', '1X2 TEMPO 1|2',  
        'DOPPIA CHANCE IN|1X', 'DOPPIA CHANCE IN|12', 'DOPPIA CHANCE IN|X2',  
        'UNDER/OVER 1.5|UNDER', 'UNDER/OVER 1.5|OVER',     
        'UNDER/OVER 2.5|UNDER', 'UNDER/OVER 2.5|OVER',   
        'UNDER/OVER 3.5|UNDER', 'UNDER/OVER 3.5|OVER',
        'GOL/NOGOL|GOL', 'GOL/NOGOL|NOGOL',       
    ],
    13 : [
        '1X2|1', '1X2|X', '1X2|2',
        '1X2 1T|1', '1X2 1T|X', '1X2 1T|2',  
        '1X|1X', '12|12', '1X|1X',   
        'MULTIGOL 1-2 |SI', 'MULTIGOL 1-2 |NO',     
        'MULTIGOL 2-3 |SI', 'MULTIGOL 2-3 |NO',     
        'MULTIGOL 3-4 |SI', 'MULTIGOL 3-4 |NO',
        'GG/NG|GOAL', 'GG/NG|NOGOAL',       
    ],
    14 : [
        '1X2|1', '1X2|X', '1X2|2', 
        'Primo Tempo|1-Primo Tempo', 'Primo Tempo|X-Primo Tempo', 'Primo Tempo|2-Primo Tempo', 
        'Doppia Chance|1X DC', 'Doppia Chance|12 DC', 'Doppia Chance|X2 DC',  
        'Over/Under 1.5|Under 1.5', 'Over/Under 1.5|Over 1.5',       
        'Over/Under 2.5|Under 2.5', 'Over/Under 2.5|Over 2.5',       
        'Over/Under 3.5|Under 3.5', 'Over/Under 3.5|Over 3.5',       
        'Gol/No Gol|GG', 'Gol/No Gol|NG',       
    ],
    15 : [
        '1X2|1', '1X2|X', '1X2|2',       
        'Solo primo tempo|1', 'Solo primo tempo|X', 'Solo primo tempo|2',  
        'Doppia chance|1X', 'Doppia chance|12', 'Doppia chance|X2',  
        'under/over 1.5|under 1.5 gol', 'under/over 1.5|over 1.5 gol',       
        'under/over 2.5|under 2.5 gol', 'under/over 2.5|over 2.5 gol',       
        'under/over 3.5|under 3.5 gol', 'under/over 3.5|over 3.5 gol',
        'Goal/No Goal|goal', 'Goal/No Goal|no goal',       
    ],
}

PDF_QUOTE_TYPES_NAMES = [
    'ESITO FINALE 1X2|1',
    'ESITO FINALE 1X2|X',
    'ESITO FINALE 1X2|2',
    'ESITO FINALE 1° TEMPO 1X2|1',
    'ESITO FINALE 1° TEMPO 1X2|X',
    'ESITO FINALE 1° TEMPO 1X2|2',
    'DOPPIA CHANCE|1X',
    'DOPPIA CHANCE|12',
    'DOPPIA CHANCE|X2',
    'UNDER/OVER 1,5|U',
    'UNDER/OVER 1,5|O',
    'UNDER/OVER 2,5|U',
    'UNDER/OVER 2,5|O',
    'UNDER/OVER 3,5|U',
    'UNDER/OVER 3,5|O',
    'GOAL/NOGOAL|GG',
    'GOAL/NOGOAL|NG',
]

           
QUOTE_URL = "http://www.tradingm3.com/failbook/Sure/suresystem/service/bvaquoteall.aspx?book={dealer_id}&sport=0"

#DJANGO APSCHEDULER
APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

AUTHENTICATION_BACKENDS = ['apps.authentication.module.EmailBackend']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

PHONENUMBER_DEFAULT_REGION = 'IT'