from openai import OpenAI
import os
from app.config.config import current_config

def create_speech(text,output_path=None):
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
            base_url = current_config.API_URL,
            api_key = current_config.API_KEY,
        )

        response = client.audio.speech.create(
            model = "Step-Audio-TTS-3B",
            input = text,
            voice = "alloy",
        )
        
        if output_path:
            # 如果只提供了文件名，使用默认目录
            if not os.path.dirname(output_path):
                output_path = os.path.join(current_config.TTS_OUTPUT_FOLDER, output_path)
                print(output_path)
            
            # 保存音频文件
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return {"success": True, "file_path": output_path}
    except Exception as e:
        return {"error": str(e)}
