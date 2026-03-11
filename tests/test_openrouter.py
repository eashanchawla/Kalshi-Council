import unittest
from unittest.mock import patch, MagicMock
from backend.services.openrouter import OpenRouterClient, ChatResponse
import os

class TestOpenRouterClient(unittest.TestCase):
    @patch('backend.services.openrouter.settings')
    @patch('requests.post')
    def test_chat_success(self, mock_post, mock_settings):
        # Setup mocks
        mock_settings.OPENROUTER_API_KEY = "test_key"
        mock_settings.OPENROUTER_DEFAULT_MODEL = "test_model"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello!"}}],
            "model": "test_model",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        mock_post.return_value = mock_response

        # Initialize client
        client = OpenRouterClient(api_key="test_key")

        # Call chat
        response = client.chat(messages=[{"role": "user", "content": "Hi"}])

        # Assertions
        self.assertIsInstance(response, ChatResponse)
        self.assertEqual(response.content, "Hello!")
        self.assertEqual(response.usage.total_tokens, 15)
        self.assertEqual(response.model, "test_model")

        # Verify post call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['model'], "test_model")
        self.assertEqual(kwargs['json']['messages'], [{"role": "user", "content": "Hi"}])

    @patch('backend.services.openrouter.settings')
    @patch('requests.post')
    def test_chat_with_system_and_custom_model(self, mock_post, mock_settings):
        # Setup mocks
        mock_settings.OPENROUTER_API_KEY = "test_key"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "System recognized."}}],
            "model": "custom_model",
            "usage": {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10}
        }
        mock_post.return_value = mock_response

        client = OpenRouterClient(api_key="test_key")

        response = client.chat(
            messages=[{"role": "user", "content": "Hi"}],
            model="custom_model",
            system="Be a helper"
        )

        self.assertEqual(response.content, "System recognized.")

        # Verify payload contains system message
        args, kwargs = mock_post.call_args
        messages = kwargs['json']['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], {"role": "system", "content": "Be a helper"})
        self.assertEqual(kwargs['json']['model'], "custom_model")

if __name__ == '__main__':
    unittest.main()
