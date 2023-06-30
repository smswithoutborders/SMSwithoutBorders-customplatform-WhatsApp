"""Configurations Module"""

import os

# Environment Variables
MODE = os.environ.get("MODE")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
ORIGINS = os.environ.get("ORIGINS")
SSL_PORT = os.environ.get("SSL_PORT")
SSL_CERTIFICATE = os.environ.get("SSL_CERTIFICATE")
SSL_KEY = os.environ.get("SSL_KEY")
SSL_PEM = os.environ.get("SSL_PEM")
WHATSAPP_CREDENTIALS = os.environ.get("WHATSAPP_CREDENTIALS")


class BaseConfig:
    """Base Configurations"""

    HOST = HOST
    PORT = PORT
    ORIGINS = ORIGINS
    WHATSAPP_CREDENTIALS = WHATSAPP_CREDENTIALS


class Production(BaseConfig):
    """Production Configurations"""

    SSL_PORT = SSL_PORT
    SSL_CERTIFICATE = SSL_CERTIFICATE
    SSL_KEY = SSL_KEY
    SSL_PEM = SSL_PEM

    COOKIE_SECURE = True


class Development(BaseConfig):
    """Development Configurations"""

    SSL_PORT = SSL_PORT
    SSL_CERTIFICATE = SSL_CERTIFICATE or ""
    SSL_KEY = SSL_KEY or ""
    SSL_PEM = SSL_PEM or ""

    COOKIE_SECURE = False


# Choose the appropriate configuration based on the environment
if MODE and MODE.lower() == "production":
    Configurations = Production
else:
    Configurations = Development
