from flask import Flask, json, jsonify, request, send_file
from flask_range_request import RangeRequest
import os

app = Flask(__name__)

# 音频文件映射关系
# AUDIO_MAPPING = {
#     "516265250": "听妈妈的话.mp3",
#     "516265274": "晴天.mp3",
#     "516265291": "月半小夜曲.mp3",
#     "516265306": "梦醒时分.mp3",
#     "516265314": "稻香.mp3",
#     "516265328": "红日.mp3",
#     "516265342": "蓝莲花.mp3",
#     "516265359": "audio.mp3",
#     "516265371": "audio.mp3",
#     "516265405": "audio.mp3"
# }
AUDIO_MAPPING = {
    "516265250": "audio.mp3",
    "516265274": "audio.mp3",
    "516265291": "audio.mp3",
    "516265306": "audio.mp3",
    "516265314": "audio.mp3",
    "516265328": "audio.mp3",
    "516265342": "audio.mp3",
    "516265359": "audio.mp3",
    "516265371": "audio.mp3",
    "516265405": "audio.mp3"
}

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
@app.route('/api/story_url_media', methods=['GET'])
def get_story_url_media():
    # 获取请求参数中的id
    story_id = request.args.get('id')
    
    # 检查是否存在对应的音频文件
    if story_id in AUDIO_MAPPING:
        file_path = os.path.join('mp3', AUDIO_MAPPING[story_id])
        
        if os.path.exists(file_path):
            # 使用 Flask-RangeRequest 处理 Range 请求
            response = RangeRequest(
                file_path,
                mimetype='audio/mpeg',
                as_attachment=False
            )
            response.headers['Connection'] = 'keep-alive'
            response.headers['Cache-Control'] = 'max-age=2592000'
            return response
        else:
            return jsonify({"code": 1, "ret": 1, "msg": "audio file not found"}), 404
    else:
        return jsonify({"code": 1, "ret": 1, "msg": "story not found"}), 404

if __name__ == '__main__':
    # 启用调试模式，默认端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)