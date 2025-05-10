import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed'
    DEBUG = False
    UPLOAD_FOLDER = os.path.join('uploads', 'image')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    BASE_URL = 'http://172.26.25.10:5000'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 