from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4g=c%jsu=urh2-bu3x8$!pfus7(fr7e+=zz73(=7nx3gj+g@ft'

try:
    from .local import *
except ImportError:
    pass

## SENTRY STUFF ##
sentry_sdk.init(
    dsn="https://2c576dce6ee644af989cc6c361bc01a1@o436418.ingest.sentry.io/5397569",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)