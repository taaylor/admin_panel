import os

DATABASES = {
    "default": {
        "ENGINE": str(os.getenv("ENGINE")),
        "NAME": str(os.getenv("POSTGRES_DBNAME")),
        "USER": str(os.getenv("POSTGRES_USER")),
        "PASSWORD": str(os.getenv("POSTGRES_PASSWORD")),
        "HOST": str(os.getenv("POSTGRES_HOST")),
        "PORT": str(os.getenv("POSTGRES_PORT")),
        "OPTIONS": {"options": str(os.getenv("POSTGRES_OPTIONS"))},
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'formatters': {
#         'default': {
#             'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
#         },
#     },
#     'handlers': {
#         'debug-console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'default',
#             'filters': ['require_debug_true'],
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['debug-console'],
#             'propagate': False,
#         }
#     },
# }
