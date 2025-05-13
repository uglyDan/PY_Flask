from flask import Flask
import os

from app.config.config import current_config
from app.utils.file_utils import ensure_upload_folder_exists

def create_app():
    """创建并初始化Flask应用"""
    app = Flask(__name__)
    app.config.from_object(current_config)
    
    # 确保上传文件夹存在
    ensure_upload_folder_exists()
    
    # 注册蓝图
    from app.routes.upload import upload_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(api_bp)
    
    return app 