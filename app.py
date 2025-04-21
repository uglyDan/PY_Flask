from flask import Flask, json, jsonify, request, send_file
import os
from werkzeug.utils import secure_filename

from ai_img import get_image_caption

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_image', methods=['POST'])
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
        # 如果文件名与已存在的文件名相同，则重命名
        if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
            filename = f"{filename.split('.')[0]}_copy.{filename.split('.')[-1]}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print("保存路径:", file_path)
        file.save(file_path)
        print("文件保存成功")
        caption = get_image_caption(file_path)
        print("图片描述:", caption)
        # 只提取描述文本
        caption_text = caption.get('caption', '') if isinstance(caption, dict) else ''
        # 将图片描述写入jsonify
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

@app.route('/api/list', methods=['GET'])
def get_list():
    with open ('api_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# 表端 首页
@app.route('/api/data', methods=['GET'])
def get_data():
    # 从json文件读取数据
    with open('api_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# 表端 故事列表
@app.route('/api/story', methods=['GET'])
def get_story():
    # jump_value 为故事类型id
    jump_value = request.args.get('jump_value')
    
    
    with open ('api_story.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 根据 jump_value 在 data 里匹配对应的 story
    if jump_value in data['data']:
        return jsonify(
            {
                "code": 0,
                "ret": 0,
                "msg": "success",
                "data": {
                    "count": data['data'][jump_value]['count'],
                    "current_page": data['data'][jump_value]['current_page'],
                    "album": data['data'][jump_value]['album'],
                    "tracks": data['data'][jump_value]['tracks']
                }
            }
        )
    else:
        return jsonify({"code": 1, "ret": 1, "msg": "story not found"}), 404

# 表端 故事播放
@app.route('/api/story_url', methods=['GET'])
def get_story_url():
    # 获取请求参数中的id
    story_id = request.args.get('id')
    
    # 读取json文件
    with open('api_story.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 遍历所有故事类型中的tracks
    for story_type in data['data'].values():
        if 'tracks' in story_type:
            for item in story_type['tracks']:
                if item['track_id'] == int(story_id):
                    return jsonify({
                        "code": 0, 
                        "ret": 0, 
                        "msg": "success", 
                        "data": {
                            "id": item['track_id'],
                            "duration": item['duration'],
                            "play_size": item['play_size'],
                            "play_url": item['play_url']                
                        }
                    })
    
    return jsonify({"code": 1, "ret": 1, "msg": "story not found"}), 404

# 表端 故事播放 媒体流 content-type:audio/mpeg
@app.route('/api/story_url_media/<filename>', methods=['GET'])
def get_story_url_media(filename):
    file_path = os.path.join('mp3', filename)
    
    if not os.path.isfile(file_path):
        return jsonify({"code": 1, "ret": 1, "msg": "audio file not found"}), 404
    
    response = send_file(
        file_path,
        mimetype='audio/mpeg',
        as_attachment=False,
        conditional=True
    )
    
    # 确保使用正确的缓存控制和连接头
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Accept-Ranges'] = 'bytes'
    
    return response

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == '__main__':
    # 启用调试模式，默认端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)
    