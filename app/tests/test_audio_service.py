import unittest
from app.services.audio_service import get_audio_description

class TestAudioService(unittest.TestCase):
    def test_get_audio_description_success(self):
        # 测试用例1：使用有效的音频URL
        test_audio_url = "https://alist.feldan1.top:9443/d/temp/ou/test.MP3"
        result = get_audio_description(test_audio_url)
        print(result)
        
        # 验证返回结果不是错误信息
        self.assertNotIn("error", result)
    def test_get_audio_description_invalid_url(self):
        # 测试用例2：使用无效的URL
        invalid_url = "invalid-url"
        result = get_audio_description(invalid_url)
        print(result) 
        
        # 验证返回错误信息
        self.assertIn("error", result)
        
    def test_get_audio_description_custom_params(self):
        # 测试用例3：使用自定义参数
        test_audio_url = "https://alist.feldan1.top:9443/d/temp/ou/test.MP3"
        result = get_audio_description(
            audio_url=test_audio_url,
            model="Qwen2-Audio-7B-Instruct",
            max_tokens=256
        )
        print(result)
        # 验证返回结果不是错误信息
        self.assertNotIn("error", result)

if __name__ == '__main__':
    unittest.main() 