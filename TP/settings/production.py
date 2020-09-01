from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4g=c%jsu=urh2-bu3x8$!pfus7(fr7e+=zz73(=7nx3gj+g@ft'

try:
    from .local import *
except ImportError:
    pass
