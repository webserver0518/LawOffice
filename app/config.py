import os

class Config:
    """הגדרות בסיס משותפות לכל הסביבות"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    TEMPLATES_AUTO_RELOAD = True
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable static caching by default
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your@email.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "yourpassword")


class DevelopmentConfig(Config):
    """הגדרות לפיתוח"""
    DEBUG = True
    ENV = "development"
    SEND_FILE_MAX_AGE_DEFAULT = 0


class ProductionConfig(Config):
    """הגדרות לפרודקשן"""
    DEBUG = False
    ENV = "production"
    SEND_FILE_MAX_AGE_DEFAULT = 3600  # Cache static files for 1 hour
