import requests
from requests_toolbelt import MultipartEncoder
import os
from app.config.config import current_config

API_URL = "https://ai.gitee.com/v1/images/caption"
headers = {
    "Authorization": f"Bearer {current_config.API_KEY}"
}

def get_image_caption(image_path, model="Florence-2-large", caption_level=1):
    """
    获取图片描述
    
    Args:
        image_path (str): 图片文件路径
        model (str): 使用的模型名称，默认为 Florence-2-large
        caption_level (int): 描述级别，默认为1
        
    Returns:
        dict: API返回的结果
    """
    try:
        if not os.path.exists(image_path):
            return {"error": "文件不存在"}
            
        with open(image_path, "rb") as image_file:
            encoder = MultipartEncoder({
                "model": model,
                "image": (os.path.basename(image_path), image_file, "image/jpg"),
                "caption_level": str(caption_level)
            })
            headers["Content-Type"] = encoder.content_type
            response = requests.post(API_URL, headers=headers, data=encoder)
            return response.json()
    except Exception as e:
        return {"error": str(e)} 