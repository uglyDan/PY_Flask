import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed'
    DEBUG = False
    UPLOAD_FOLDER = os.path.join('uploads', 'image')
    AUDIO_UPLOAD_FOLDER = os.path.join('uploads', 'audio')
    TTS_OUTPUT_FOLDER = os.path.join('uploads', 'tts')
    ALLOWED_EXTENSIONS = {'jpg', 'mp3'}
    BASE_URL = 'http://172.26.25.10:5000'
    
    # API配置
    API_URL = "https://ai.gitee.com/v1"
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    API_KEY = "7CNIDO2WCXSMVYQXRVC2IDBUFGMGH1U0TFXLIQ1V"

class ProductionConfig(BaseConfig):
    DEBUG = False
    API_KEY = "HIG3RE8ZBAIRKDJELB0D5E0YP1PEIKER2EMHAU1T"
# 直接导出配置实例而不是类
development_config = DevelopmentConfig()
production_config = ProductionConfig()

# 默认使用开发环境配置
current_config = development_config 