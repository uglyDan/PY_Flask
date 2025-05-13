from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os

from app.services.image_service import get_image_caption
from app.utils.file_utils import allowed_file, get_unique_filename
from app.config.config import current_config

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/api/upload_image', methods=['POST'])
def upload_image():
    print("收到上传图片请求")
    print("请求头:", request.headers)
    
    if 'file' not in request.files:
        print("请求中没有文件部分")
        return jsonify({"code": 1, "msg": "No file part"}), 400
    
    file = request.files['file']
    print("文件名:", file.filename)
    print("文件类型:", file.content_type)
    
    if file.filename == '':
        print("文件名为空")
        return jsonify({"code": 1, "msg": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_config.UPLOAD_FOLDER
        print("upload_folder:", upload_folder)
        
        # 确保上传目录存在
        os.makedirs(upload_folder, exist_ok=True)
        
        # 获取唯一文件名
        filename = get_unique_filename(upload_folder, filename)
        file_path = os.path.join(upload_folder, filename)
        
        print("保存路径:", file_path)
        file.save(file_path)
        print("文件保存成功")
        
        caption = get_image_caption(file_path)
        print("图片描述:", caption)
        
        # 只提取描述文本
        caption_text = caption.get('caption', '') if isinstance(caption, dict) else ''
        
        # 使用配置的BASE_URL
        file_url = f"{current_config.BASE_URL}/uploads/image/{filename}"
        
        # 将图片描述写入响应
        return jsonify({
            "code": 0,
            "msg": "success",
            "data": {
                "filename": filename,
                "path": file_path,
                "url": file_url,
                "caption": caption_text
            }
        })
    
    print("文件类型不允许:", file.filename)
    return jsonify({"code": 1, "msg": "File type not allowed"}), 400

@upload_bp.route('/uploads/<file_type>/<filename>')
def uploaded_file(file_type, filename):
    from flask import send_file
    
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 根据文件类型选择不同的上传目录
    upload_folders = {
        'image': current_config.UPLOAD_FOLDER,
        'audio': current_config.AUDIO_UPLOAD_FOLDER
    }
    upload_folder = upload_folders.get(file_type, current_config.UPLOAD_FOLDER)
    file_path = os.path.join(base_dir, upload_folder, filename)
    return send_file(file_path)

