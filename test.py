import pytest
from unittest.mock import patch, MagicMock
from project1 import evaluate_startup_idea

def test_evaluate_startup_idea_with_empty_prompt():
    result = evaluate_startup_idea("")
    assert result == "Please enter your startup idea to get an evaluation."

@patch("project1.model")
def test_evaluate_startup_idea_success(mock_model):
    mock_convo = MagicMock()
    mock_convo.send_message.return_value.text = "Sample evaluation response."
    mock_model.start_chat.return_value = mock_convo

    prompt = "An AI tool that matches pet owners with ideal pets based on their habits."
    result = evaluate_startup_idea(prompt)
    assert "Sample evaluation response." in result

@patch("project1.model")
def test_evaluate_startup_idea_api_failure(mock_model):
    mock_model.start_chat.side_effect = Exception("API error")

    result = evaluate_startup_idea("A startup idea")
    assert "❌ **Error occurred:** API error" in result