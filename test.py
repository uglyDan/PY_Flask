from openai import OpenAI
import os

API_URL = "https://ai.gitee.com/v1"
API_KEY = "HIG3RE8ZBAIRKDJELB0D5E0YP1PEIKER2EMHAU1T"
DEFAULT_OUTPUT_DIR = "./uploads/audio"

def create_speech(text, model="Step-Audio-TTS-3B", voice="alloy", output_path=None):
    """
    将文本转换为语音
    
    Args:
        text (str): 要转换的文本内容
        model (str): 使用的模型名称，默认为 Step-Audio-TTS-3B
        voice (str): 语音类型，默认为 alloy
        output_path (str, optional): 输出音频文件的路径，如果只提供文件名，将保存在默认目录
        
    Returns:
        dict: 包含音频数据或错误信息的字典
    """
    try:
        client = OpenAI(
            base_url=API_URL,
            api_key=API_KEY,
        )

        response = client.audio.speech.create(
            model=model,
            input=text,
            voice=voice,
        )
        
        if output_path:
            # 如果只提供了文件名，使用默认目录
            if not os.path.dirname(output_path):
                output_path = os.path.join(DEFAULT_OUTPUT_DIR, output_path)
                print(output_path)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # 保存音频文件
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return {"success": True, "file_path": output_path}
            
        return {"success": True, "audio_data": response.content}
        
    except Exception as e:
        return {"error": str(e)}
    

result = create_speech("The answer to the universe is 42", output_path="output.mp3")
print(result)
file_path = result["file_path"]  # 获取保存的文件路径