from openai import OpenAI
from app.config.config import current_config

client = OpenAI(
    base_url=current_config.API_URL,
    api_key=current_config.API_KEY,
)

def get_audio_description(audio_url, model="Qwen2-Audio-7B-Instruct", max_tokens=512):
    """
    获取音频描述
    
    Args:
        audio_url (str): 音频文件的URL
        model (str): 使用的模型名称，默认为 Qwen2-Audio-7B-Instruct
        max_tokens (int): 最大生成token数，默认为512
        
    Returns:
        dict: API返回的结果
    """
    try:
        response = client.chat.completions.create(
            model=model,
            stream=True,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            extra_body={
                "top_k": -1,
            },
            frequency_penalty=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and harmless assistant. You should think step-by-step.Please respond in the same language as the audio content."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "audio_url",
                            "audio_url": {
                                "url": audio_url
                            }
                        },
                        {
                            "type": "text",
                            "text": " "
                        }
                    ]
                }
            ],
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        result = {
            "code": 0,
            "status": "success",
            "audio_description": full_response
        }
        print(result)
        return result
    except Exception as e:
        print(e)
        return {
            "code": 400,
            "status": "error",
            "error": str(e)
        }
    