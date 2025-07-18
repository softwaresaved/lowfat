"""
Django settings for lowfat project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from collections import OrderedDict
import pathlib

import decouple
from decouple import config
import dj_database_url


URL_SRC = "https://github.com/softwaresaved/lowfat"
VERSION = "1.21.0"

SETTINGS_EXPORT = [
    'URL_SRC',
    'VERSION',
]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = pathlib.Path(__file__).absolute().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)


ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*' if DEBUG else '127.0.0.1,localhost,localhost.localdomain',
    cast=decouple.Csv()
)

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'bootstrap_datepicker_plus',
    'constance',
    'constance.backends.database',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'dbbackup',
    'django_countries',
    'django_extensions',
    'imagekit',
    'import_export',
    'simple_history',
    'social_django',
    'tagulous',
]

FIRST_PARTY_APPS = [
    'lowfat',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'lowfat.urls'

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://fellows.software.ac.uk',
]

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
                'django_settings_export.settings_export',
                'social_django.context_processors.backends',
                'constance.context_processors.config',
                'lowfat.context.site',
                'lowfat.context.maintenance',
                'lowfat.context.organisation',
            ],
        },
    },
]

WSGI_APPLICATION = 'lowfat.wsgi.application'

SERIALIZATION_MODULES = {
    'xml': 'tagulous.serializers.xml_serializer',
    'json': 'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml': 'tagulous.serializers.pyyaml',
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default':
    config('DATABASE_URL',
           default='sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3')),
           cast=dj_database_url.parse)
}

# New setting in Django 3.2 - use AutoField to maintain consistency with previous versions
# See https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Logging
# https://docs.djangoproject.com/en/1.11/ref/settings/#logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR.joinpath('lowfat.log'),
            'when': 'W6',
            'backupCount': 4,
            'formatter': 'timestamped',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
    },
    'formatters': {
        'timestamped': {
            'format': '[{asctime} {levelname} {module}.{funcName}:{lineno}] {message}',
            'style': '{',
        }
    }
}

# User Model Customisation
# DO NOT DO THIS!
# READ THIS: https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model

# AUTH_USER_MODEL = 'lowfat.MyUser'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    # Default pipeline
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # Custom
    'lowfat.auth.wire_profile',
)

SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY', default='')
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET', default='')

# Should be True if running behind a reverse proxy e.g. Caddy
# See https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html#processing-redirects-and-urlopen
SOCIAL_AUTH_REDIRECT_IS_HTTPS = config('SOCIAL_AUTH_REDIRECT_IS_HTTPS', default=False)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-gb')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = "l, d F Y"  # British English style
DATETIME_FORMAT = "l, d F Y"  # British English style

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT',
                     default=BASE_DIR.joinpath('static'),
                     cast=pathlib.Path)

# Stored files
# https://docs.djangoproject.com/en/1.9/ref/settings/#media-url

MEDIA_URL = '/upload/'
MEDIA_ROOT = config('MEDIA_ROOT',
                    default=BASE_DIR.joinpath('upload'),
                    cast=pathlib.Path)

# Authentication system
# https://docs.djangoproject.com/en/1.9/topics/auth/default/

LOGIN_URL = '/login/'  # The URL where requests are redirected for login, especially when using the login_required() decorator.
LOGIN_REDIRECT_URL = '/dashboard/'


# Email backend settings
# See https://docs.djangoproject.com/en/3.0/topics/email

EMAIL_HOST = config('EMAIL_HOST', default=None)
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='no-reply@software.ac.uk' if DEBUG else decouple.Undefined)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if EMAIL_HOST is None:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    p = pathlib.Path('./tmp/emails/')
    p.mkdir(parents=True, exist_ok=True)
    EMAIL_FILE_PATH = config('EMAIL_FILE_PATH', default=p)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)

    EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS',
                           default=(EMAIL_PORT == 587),
                           cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL',
                           default=(EMAIL_PORT == 465),
                           cast=bool)

# Subject-line prefix for email messages sent
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='')

# A list of all the people who get code error notifications.
ADMINS = [
    ('admin', 'admin@software.ac.uk'),
]


# Backup
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location':
    config('DBBACKUP_STORAGE_LOCATION',
           default=BASE_DIR.joinpath('backups'),
           cast=pathlib.Path),
}

DBBACKUP_GPG_ALWAYS_TRUST = True

# This variable need to be filled for --encrypt or --decrypt work properly.
DBBACKUP_GPG_RECIPIENT = config('DBBACKUP_GPG_RECIPIENT', default='')


# Run time variables
# Powered by Constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_CONFIG = OrderedDict([
    ("ORGANISATION_NAME", (
        "Software Sustainability Institute",
        "Default organisation name.",
    )),
    ("ORGANISATION_WEBSITE", (
        "https://www.software.ac.uk/",
        "Default organisation website.",
    )),
    ("FUNDS_FROM_DEFAULT", (
        "F",
        "Default funds used for expense.",
    )),
    ("GRANTS_DEFAULT", (
        "SSI3",
        "Default grant for expenses.",
    )),
    ("FELLOWS_MANAGEMENT_EMAIL", (
        "fellows-management@software.ac.uk",
        "Contact address to fellows management staffs.",
    )),
    ("FUND_FINANCE_EMAIL", (
        "finance@software.ac.uk",
        "Finance address to receive payment choice updates.",
    )),
    ("FUND_FINANCE_EMAIL_CC", (
        "fellows-management@software.ac.uk",
        "CC Address to receive payment choice updates",
    )),
    ("ONETIME_APPROVAL_EMAIL", (
        "fellows-management@software.ac.uk",
        "Address for approval of one-time requests.",
    )),
    ("WEBSITE_GATEKEEPER", (
        "Gatekeeper Name",
        "Name of website gatekeeper, e.g. 'John'.",
    )),
    ("WEBSITE_GATEKEEPER_EMAIL", (
        "gatekeeper@software.ac.uk",
        "Email of website gatekeeper, e.g. 'john@software.ac.uk'.",
    )),
    ("STAFFS_EMAIL", (
        "['Software Sustainability Institute <fellows-management@software.ac.uk>']",
        "Contact address of staffs, e.g. ['John <john@example.com>', 'Mary <mary@example.com>'].",
    )),
    ("STAFFS_EMAIL", (
        "['Software Sustainability Institute <fellows-management@software.ac.uk>']",
        "Contact address of staffs, e.g. ['John <john@example.com>', 'Mary <mary@example.com>'].",
    )),
    ("STAFF_EMAIL_NOTIFICATION", (
        False,
        "Notification to staffs by email.",
    )),
    ("STAFF_EMAIL_REMINDER", (
        False,
        "Reminder staffs of pending tasks by email.",
    )),
    ("DAYS_TO_ANSWER_BACK", (
        3,
        "Days to answer back before receive a email reminder.",
    )),
    ("STAFF_EMAIL_FOLLOW_UP", (
        False,
        "Reminder staff of tasks to follow up with by email.",
    )),
    ("FOLLOW_UP_DAY", (
        0,
        "Weekday to send follow up email to staff. 0 for Monday.",
    )),
    ("CLAIMANT_EMAIL_NOTIFICATION", (
        False,
        "Notification to claimant by email.",
    )),
    ("MAINTENANCE_DAY", (
        4,
        "Day when maintenance normally take place.",
    )),
    ("MAINTENANCE_HOUR", (
        9,
        "Hour when maintenance normally take placece.",
    )),
    ("FELLOWSHIP_EXPENSES_END_DAY", (
        31,
        "Day deadline that expenses must be submitted.",
    )),
    ("FELLOWSHIP_EXPENSES_END_MONTH", (
        3,
        "Month deadline that expenses must be submitted.",
    )),
    ("PRE_APPROVED_FUNDING_REQUEST_BUDGET", (
        250,
        "Maximum budget for pre approved funding requests, e.g. 250.",
    )),
    ("CALENDAR_ACCESS_TOKEN", (
        "lKI7BSE7JCWaIw54xywVZy8zRTKLqOM3",
        "Token to access the calendar.",
    )),
])


# Flatpages

SITE_ID = 1
