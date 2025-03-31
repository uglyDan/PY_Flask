from flask import Flask, json, jsonify, request, send_file
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    # 启用调试模式，默认端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)