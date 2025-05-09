import os
from app.config.config import config

def allowed_file(filename):
    """检查文件扩展名是否在允许列表中"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config['default'].ALLOWED_EXTENSIONS

def get_unique_filename(upload_folder, filename):
    """获取唯一文件名，避免文件名冲突"""
    if os.path.exists(os.path.join(upload_folder, filename)):
        filename = f"{filename.split('.')[0]}_copy.{filename.split('.')[-1]}"
    return filename

def ensure_upload_folder_exists():
    """确保上传文件夹存在"""
    upload_folder = config['default'].UPLOAD_FOLDER
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder) 