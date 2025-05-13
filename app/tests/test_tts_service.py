import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
from app.services.tts_service import create_speech

class TestTTSService(unittest.TestCase):
    
    @patch('app.services.tts_service.OpenAI')
    def test_create_speech_basic(self, mock_openai):
        # 设置模拟的OpenAI客户端和响应
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = b'audio_content'
        mock_client.audio.speech.create.return_value = mock_response
        
        # 调用函数
        result = create_speech("测试文本")
        
        # 验证
        self.assertTrue(result["success"])
        self.assertEqual(result["audio_data"], b'audio_content')
        mock_client.audio.speech.create.assert_called_once_with(
            model="Step-Audio-TTS-3B",
            input="测试文本",
            voice="alloy"
        )
    
    @patch('app.services.tts_service.OpenAI')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_create_speech_with_output_path(self, mock_makedirs, mock_file, mock_openai):
        # 设置模拟
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = b'audio_content'
        mock_client.audio.speech.create.return_value = mock_response
        
        # 调用函数
        result = create_speech("测试文本", output_path="/path/to/output.mp3")
        
        # 验证
        self.assertTrue(result["success"])
        self.assertEqual(result["file_path"], "/path/to/output.mp3")
        mock_makedirs.assert_called_once_with(os.path.dirname("/path/to/output.mp3"), exist_ok=True)
        mock_file.assert_called_once_with("/path/to/output.mp3", 'wb')
        mock_file().write.assert_called_once_with(b'audio_content')
    
    @patch('app.services.tts_service.OpenAI')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_create_speech_with_filename_only(self, mock_makedirs, mock_file, mock_openai):
        # 设置模拟
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = b'audio_content'
        mock_client.audio.speech.create.return_value = mock_response
        
        # 调用函数
        result = create_speech("测试文本", output_path="output.mp3")
        
        # 验证
        expected_path = os.path.join("/PY_Flask/uploads/audio", "output.mp3")
        self.assertTrue(result["success"])
        self.assertEqual(result["file_path"], expected_path)
        mock_makedirs.assert_called_once_with(os.path.dirname(expected_path), exist_ok=True)
        mock_file.assert_called_once_with(expected_path, 'wb')
        mock_file().write.assert_called_once_with(b'audio_content')
    
    @patch('app.services.tts_service.OpenAI')
    def test_create_speech_with_custom_params(self, mock_openai):
        # 设置模拟
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = b'audio_content'
        mock_client.audio.speech.create.return_value = mock_response
        
        # 调用函数
        result = create_speech("测试文本", model="custom-model", voice="custom-voice")
        
        # 验证
        self.assertTrue(result["success"])
        mock_client.audio.speech.create.assert_called_once_with(
            model="custom-model",
            input="测试文本",
            voice="custom-voice"
        )
    
    @patch('app.services.tts_service.OpenAI')
    def test_create_speech_error_handling(self, mock_openai):
        # 设置模拟发生异常
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.audio.speech.create.side_effect = Exception("API调用失败")
        
        # 调用函数
        result = create_speech("测试文本")
        
        # 验证
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API调用失败")

if __name__ == "__main__":
    unittest.main()
