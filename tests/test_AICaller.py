import os

import pytest
from unittest.mock import patch
from coverage_ai.AICaller import AICaller


class TestAICaller:
    @pytest.fixture
    def ai_caller(self):
        return AICaller("test-model", "test-api")

    @patch("coverage_ai.AICaller.AICaller.call_model")
    def test_call_model_simplified(self, mock_call_model):
        # Set up the mock to return a predefined response
        mock_call_model.return_value = ("Hello world!", 2, 10)
        prompt = {"system": "", "user": "Hello, world!"}

        ai_caller = AICaller("test-model", "test-api")
        # Explicitly provide the default value of max_tokens
        response, prompt_tokens, response_tokens = ai_caller.call_model(
            prompt, max_tokens=4096
        )

        # Assertions to check if the returned values are as expected
        assert response == "Hello world!"
        assert prompt_tokens == 2
        assert response_tokens == 10

        # Check if call_model was called correctly
        mock_call_model.assert_called_once_with(prompt, max_tokens=4096)

    @patch("coverage_ai.AICaller.litellm.completion")
    def test_call_model_with_error(self, mock_completion, ai_caller):
        # Set up mock to raise an exception
        mock_completion.side_effect = Exception("Test exception")
        prompt = {"system": "", "user": "Hello, world!"}
        # Call the method and handle the exception
        with pytest.raises(Exception) as exc_info:
            ai_caller.call_model(prompt)

        assert str(exc_info.value) == "Test exception"

    @patch("coverage_ai.AICaller.litellm.completion")
    def test_call_model_error_streaming(self, mock_completion, ai_caller):
        # Set up mock to raise an exception
        mock_completion.side_effect = ["results"]
        prompt = {"system": "", "user": "Hello, world!"}
        # Call the method and handle the exception
        with pytest.raises(Exception) as exc_info:
            ai_caller.call_model(prompt)

        assert str(exc_info.value) == "list index out of range"

    @patch("coverage_ai.AICaller.litellm.completion")
    @patch.dict(os.environ, {"WANDB_API_KEY": "test_key"})
    @patch("coverage_ai.AICaller.Trace.log")
    def test_call_model_wandb_logging(self, mock_log, mock_completion, ai_caller):
        mock_completion.return_value = [
            {"choices": [{"delta": {"content": "response"}}]}
        ]
        prompt = {"system": "", "user": "Hello, world!"}
        with patch("coverage_ai.AICaller.litellm.stream_chunk_builder") as mock_builder:
            mock_builder.return_value = {
                "choices": [{"message": {"content": "response"}}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 10},
            }
            response, prompt_tokens, response_tokens = ai_caller.call_model(prompt)
            assert response == "response"
            assert prompt_tokens == 2
            assert response_tokens == 10
            mock_log.assert_called_once()

    @patch("coverage_ai.AICaller.litellm.completion")
    def test_call_model_api_base(self, mock_completion, ai_caller):
        mock_completion.return_value = [
            {"choices": [{"delta": {"content": "response"}}]}
        ]
        ai_caller.model = "openai/test-model"
        prompt = {"system": "", "user": "Hello, world!"}
        with patch("coverage_ai.AICaller.litellm.stream_chunk_builder") as mock_builder:
            mock_builder.return_value = {
                "choices": [{"message": {"content": "response"}}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 10},
            }
            response, prompt_tokens, response_tokens = ai_caller.call_model(prompt)
            assert response == "response"
            assert prompt_tokens == 2
            assert response_tokens == 10

    @patch("coverage_ai.AICaller.litellm.completion")
    def test_call_model_with_system_key(self, mock_completion, ai_caller):
        mock_completion.return_value = [
            {"choices": [{"delta": {"content": "response"}}]}
        ]
        prompt = {"system": "System message", "user": "Hello, world!"}
        with patch("coverage_ai.AICaller.litellm.stream_chunk_builder") as mock_builder:
            mock_builder.return_value = {
                "choices": [{"message": {"content": "response"}}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 10},
            }
            response, prompt_tokens, response_tokens = ai_caller.call_model(prompt)
            assert response == "response"
            assert prompt_tokens == 2
            assert response_tokens == 10

    def test_call_model_missing_keys(self, ai_caller):
        prompt = {"user": "Hello, world!"}
        with pytest.raises(KeyError) as exc_info:
            ai_caller.call_model(prompt)
        assert (
            str(exc_info.value)
            == "\"The prompt dictionary must contain 'system' and 'user' keys.\""
        )
