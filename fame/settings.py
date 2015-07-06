"""
Django settings for fame project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p)_s!7lt!l6e!&05s8#g^ch%uh28rjtm8zun^^8z928rn*9k@k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_countries',  # https://pypi.python.org/pypi/django-countries
    'timezone_field',  # https://github.com/mfogel/django-timezone-field
    'suit_redactor',  # http://django-suit.readthedocs.org/en/latest/wysiwyg.html
    'fame',
    'competition',
    'media',
    'artist',
    'socialconnector',
    'userprofile',

    'social.apps.django_app.default',  # http://psa.matiasaguirre.net/docs/index.html
    'rest_framework',  # http://www.django-rest-framework.org/
    'blog',
    'content',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'fame.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                # 'userprofile.context_processors.check_profile'
            ],
        },
    },
]

WSGI_APPLICATION = 'fame.wsgi.application'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.template.context_processors.media',
    'social.apps.django_app.context_processors.backends',
    'social.backends.twitter',
    'social.apps.django_app.context_processors.login_redirect',
)


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'fame')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
# )
MEDIA_ROOT = os.path.join(BASE_DIR, 'server_media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.dropbox.DropboxOAuth2',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.dropbox.DropboxOAuth2',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.vimeo.VimeoOAuth2',
    'social.backends.spotify.SpotifyOAuth2',
    'social.backends.mixcloud.MixcloudOAuth2',
    'social.backends.instagram.InstagramOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '535030322236-k5s1pcagr92d63m7kolei8j9rarcm4sq.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '6upMaUQjc2a64ZXiITl0yVyA'
SOCIAL_AUTH_TWITTER_KEY = 'miBYJOOJEFKgSKd6eGcHxk3bu'
SOCIAL_AUTH_TWITTER_SECRET = 'eKkt0AimnHoQaod5Vulz1WqkNCF0KY2OayinbVPMEcYPjerjYM'
SOCIAL_AUTH_FACEBOOK_KEY = '896661813714026'
SOCIAL_AUTH_FACEBOOK_SECRET = '2192c3a1b4fcdc5e0f7747372faaca45'
SOCIAL_AUTH_SOUNDCLOUD_KEY = 'a8ec4ade20001df3f84f7e3655e98f50'
SOCIAL_AUTH_SOUNDCLOUD_SECRET = 'baaf2a08fa7e381cfa5372ec111b742f'
SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = '5cnahv6icn8d13u'
SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = 'u33gwehwwyw31qg'

SOCIAL_AUTH_VIMEO_KEY = '2ba4e289b126abc35393945ca39b0f776c0d7d60'
SOCIAL_AUTH_VIMEO_SECRET = 'xFNiUgTBt8+SevybTAA+X9nI8yZvGqKz6HrQReDgS6gnrMWEZ1grTZT4L0vIcdXrFvsKnI/AAo/Lk76koF+13XTAVyO+5+Em5OUR3SLS9YhWE25zX+QVuOsWvDHiTdpw'

SOCIAL_AUTH_SPOTIFY_KEY = '141696ab3b974e72aa1f90d57abdbae1'
SOCIAL_AUTH_SPOTIFY_SECRET = '4366346820a04e31b708ecede2b575b1'
SOCIAL_AUTH_MIXCLOUD_KEY = 'VdhvaMrVtLwAF92MS5'
SOCIAL_AUTH_MIXCLOUD_SECRET = '5k8KGUrVwPwaZyywSg4yQ7DBzrGcxWs5'
SOCIAL_AUTH_INSTAGRAM_KEY = 'cfc23ac998ca427d8d0d3b4fca4eb7cc'
SOCIAL_AUTH_INSTAGRAM_SECRET = '678fb9423f1a400cb416bddc697052fb'

SESSION_SERIALIZER ='django.contrib.sessions.serializers.PickleSerializer'

LOGIN_REDIRECT_URL = '/user/login/'
LOGIN_URL = '/user/login/'
LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

try:
    from local_settings import *
except:
    pass