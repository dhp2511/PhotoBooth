"""
Django settings for photobooth project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import sys
import dj_database_url

sys.path.append("/myenv/src/django-verify-email/verify-email")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "photobooth.up.railway.app",
    "https://photobooth.up.railway.app/"
]
CSRF_TRUSTED_ORIGINS =['https://photobooth.up.railway.app/']
AUTH_USER_MODEL = "users.User"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "photos",
    "django.contrib.auth",
    "photos.apps.PhotosConfig",
    "users.apps.UsersConfig",
    "django_cleanup.apps.CleanupConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_user_agents",
    "django_htmx",
    "verify_email.apps.VerifyEmailConfig",
    "cloudinary_storage",
    "cloudinary",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "photobooth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "photos/templates/photos"),
            os.path.join(BASE_DIR, "photos/templates/socialaccount"),
        ],
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

WSGI_APPLICATION = "photobooth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT'),
    }
}

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=500,
        conn_health_checks=True,
    )


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTHENTICATION_CLASSES = ("allauth.account.auth_backends.AuthenticationBackend",)

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"

# Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True


SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_EMAIL_REQUIRED = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_SECRET_KEY"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}


# SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_FORMS = {
    "signup": "photos.forms.MyCustomSocialSignupForm",
}
ACCOUNT_FORMS = {"signup": "photos.forms.RegistrationForm"}


ACCOUNT_USERNAME_BLACKLIST = ["admin", "accounts", "profile", "category", "photo"]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EXPIRE_AFTER = "10h"
MAX_RETRIES = 10


VERIFICATION_SUCCESS_TEMPLATE = "email_verification/email_verification_successful.html"

VERIFICATION_FAILED_TEMPLATE = "email_verification/email_verification_failed.html"

REQUEST_NEW_EMAIL_TEMPLATE = "email_verification/request_new_email.html"

LINK_EXPIRED_TEMPLATE = "email_verification/link_expired.html"

NEW_EMAIL_SENT_TEMPLATE = "email_verification/new_email_sent.html"


LOGIN_URL = "login"


# tells user where to upload file


# https://whitenoise.readthedocs.io/en/stable/django.html#add-compression-and-caching-support
