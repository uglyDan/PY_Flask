from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
import json
from pprint import pprint

from app.services.image_service import get_image_caption
from app.utils.file_utils import allowed_file, get_unique_filename
from app.config.config import current_config
from app.services.audio_service import get_audio_description
from app.services.tts_service import create_speech
upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/api/upload_image', methods=['POST'])
def upload_image():
    print("\n" + "="*50)
    print("📷 收到上传图片请求")
    print("-"*50)
    print("📋 请求头:")
    pprint(dict(request.headers))
    
    if 'file' not in request.files:
        print("❌ 请求中没有文件部分")
        return jsonify({"code": 1, "msg": "No file part"}), 400
    
    file = request.files['file']
    print(f"📝 文件名: {file.filename}")
    print(f"📄 文件类型: {file.content_type}")
    
    if file.filename == '':
        print("❌ 文件名为空")
        return jsonify({"code": 1, "msg": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_config.UPLOAD_FOLDER
        print(f"📁 上传目录: {upload_folder}")
        
        # 确保上传目录存在
        os.makedirs(upload_folder, exist_ok=True)
        
        # 获取唯一文件名
        filename = get_unique_filename(upload_folder, filename)
        file_path = os.path.join(upload_folder, filename)
        
        print(f"💾 保存路径: {file_path}")
        file.save(file_path)
        print("✅ 文件保存成功")
        
        caption = get_image_caption(file_path)
        print("🖼️ 图片描述:")
        print(caption)
        
        # 只提取描述文本
        caption_text = caption.get('caption', '') if isinstance(caption, dict) else ''
        
        # 使用配置的BASE_URL
        file_url = f"{current_config.BASE_URL}/uploads/image/{filename}"
        
        # 将图片描述写入响应
        response = {
            "code": 0,
            "msg": "success",
            "data": {
                "filename": filename,
                "path": file_path,
                "url": file_url,
                "caption": caption_text
            }
        }
        print("📤 返回响应:")
        print(json.dumps(response, ensure_ascii=False, indent=4))
        print("="*50 + "\n")
        return jsonify(response)
    
    print(f"❌ 文件类型不允许: {file.filename}")
    return jsonify({"code": 1, "msg": "File type not allowed"}), 400


@upload_bp.route('/api/upload_audio', methods=['POST'])
def upload_audio():
    print("\n" + "="*50)
    print("🎵 收到上传音频请求")
    print("-"*50)
    print("📋 请求头:")
    pprint(dict(request.headers))
    
    if 'file' not in request.files:
        print("❌ 请求中没有文件部分")
        return jsonify({"code": 1, "msg": "No file part"}), 400
    
    file = request.files['file']
    print(f"📝 文件名: {file.filename}")
    print(f"📄 文件类型: {file.content_type}")
    
    if file.filename == '':
        print("❌ 文件名为空")
        return jsonify({"code": 1, "msg": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_config.AUDIO_UPLOAD_FOLDER
        print(f"📁 上传目录: {upload_folder}")
        
        # 确保上传目录存在
        os.makedirs(upload_folder, exist_ok=True)
        
        # 获取唯一文件名
        filename = get_unique_filename(upload_folder, filename)
        file_path = os.path.join(upload_folder, filename)
        print(f"💾 保存路径: {file_path}")
        file.save(file_path)
        print("✅ 文件保存成功")
        file_url = f"{current_config.BASE_URL}/uploads/audio/{filename}"
        print("文件url",file_url)
        # warning 测试 url 记得修改！！！
        # 测试 url http://gdust.feldan1.top:50000/uploads/audio/test.MP3
        # file_url = "https://alist.feldan1.top:9443/d/temp/ou/test.MP3"
        audio_text = get_audio_description(file_url, model="Qwen2-Audio-7B-Instruct", max_tokens=128)
        
        # 返回音频处理结果
        response = audio_text.get('audio_description', '')
        print("文本：",response)
        tmp = create_speech(response,output_path=f"{filename}")
        print("音频json：",tmp)
        
        # 返回成功响应
        response = {
            "code": 0,
            "msg": "success",
            "audio_text": response,
            
        }
        return jsonify(response)
    
    print(f"❌ 文件类型不允许: {file.filename}")
    return jsonify({"code": 1, "msg": "File type not allowed"}), 400

@upload_bp.route('/uploads/<file_type>/<filename>')
def uploaded_file(file_type, filename):
    from flask import send_file
    
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 根据文件类型选择不同的上传目录
    upload_folders = {
        'image': current_config.UPLOAD_FOLDER,
        'audio': current_config.AUDIO_UPLOAD_FOLDER,
        'tts': current_config.TTS_OUTPUT_FOLDER
    }
    upload_folder = upload_folders.get(file_type, current_config.UPLOAD_FOLDER)
    file_path = os.path.join(base_dir, upload_folder, filename)
    return send_file(file_path)

