from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os

from app.services.image_service import get_image_caption
from app.utils.file_utils import allowed_file, get_unique_filename
from app.config.config import config

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
        upload_folder = config['default'].UPLOAD_FOLDER
        
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
        
        # 将图片描述写入响应
        return jsonify({
            "code": 0,
            "msg": "success",
            "data": {
                "filename": filename,
                "path": file_path,
                "url": f"http://27.37.65.4:50000/uploads/{filename}",
                "caption": caption_text
            }
        })
    
    print("文件类型不允许:", file.filename)
    return jsonify({"code": 1, "msg": "File type not allowed"}), 400

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_file
    return send_file(os.path.join(config['default'].UPLOAD_FOLDER, filename)) 