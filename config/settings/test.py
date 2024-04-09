"""
With these settings, tests run faster.
"""

from dj_easy_log import load_loguru

from config.settings.base import *  # noqa: F403

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(  # noqa: F405
    "DJANGO_SECRET_KEY",
    default="UKNSQClo0zUtSNlFq7wJYvMcIqMZrZ2MpwAKjDtBEAbvuJosEg1frjvmNX4HmA46",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"  # noqa

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------
LOGGING["loggers"] = {  # noqa
    "rules": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": True,
    }
}

load_loguru(globals())
