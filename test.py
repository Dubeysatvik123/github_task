import pytest
from unittest.mock import patch, MagicMock, Mock
import gradio as gr
from app import evaluate_startup_idea, clear_inputs, load_example, examples


class TestEvaluateStartupIdea:
    """Tests for the evaluate_startup_idea function"""
    
    def test_empty_prompt(self):
        """Test that empty prompt returns appropriate message"""
        result = evaluate_startup_idea("")
        assert result == "Please enter your startup idea to get an evaluation."
    
    def test_whitespace_only_prompt(self):
        """Test that whitespace-only prompt returns appropriate message"""
        result = evaluate_startup_idea("   ")
        assert result == "Please enter your startup idea to get an evaluation."
    
    @patch("app.model")
    @patch("app.time.sleep")
    def test_successful_evaluation(self, mock_sleep, mock_model):
        """Test successful startup idea evaluation"""
        # Mock the conversation and response
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "## Feasibility 🔧\nThis is a feasible idea..."
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        # Mock progress
        mock_progress = MagicMock()
        
        prompt = "An AI-powered personal finance app"
        result = evaluate_startup_idea(prompt, progress=mock_progress)
        
        # Assertions
        assert "Feasibility" in result or "feasible" in result.lower()
        mock_model.start_chat.assert_called_once()
        mock_convo.send_message.assert_called_once_with(prompt)
        
        # Verify progress was called
        assert mock_progress.call_count >= 4
    
    @patch("app.model")
    def test_api_error_handling(self, mock_model):
        """Test that API errors are handled gracefully"""
        mock_model.start_chat.side_effect = Exception("API connection failed")
        
        mock_progress = MagicMock()
        result = evaluate_startup_idea("A startup idea", progress=mock_progress)
        
        assert "❌ **Error occurred:**" in result
        assert "API connection failed" in result
    
    @patch("app.model")
    def test_send_message_error(self, mock_model):
        """Test error handling when send_message fails"""
        mock_convo = MagicMock()
        mock_convo.send_message.side_effect = Exception("Rate limit exceeded")
        mock_model.start_chat.return_value = mock_convo
        
        mock_progress = MagicMock()
        result = evaluate_startup_idea("Test idea", progress=mock_progress)
        
        assert "❌ **Error occurred:**" in result
        assert "Rate limit exceeded" in result
    
    @patch("app.model")
    @patch("app.time.sleep")
    def test_progress_tracking(self, mock_sleep, mock_model):
        """Test that progress tracking works correctly"""
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Evaluation result"
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        mock_progress = MagicMock()
        
        evaluate_startup_idea("Test idea", progress=mock_progress)
        
        # Check that progress was called with expected values
        progress_calls = mock_progress.call_args_list
        assert len(progress_calls) >= 4
        
        # Verify progress descriptions
        descriptions = [call[1].get('desc', call[0][1] if len(call[0]) > 1 else None) 
                       for call in progress_calls]
        assert any("Initializing" in str(d) for d in descriptions if d)
        assert any("Complete" in str(d) for d in descriptions if d)
    
    @patch("app.model")
    def test_system_prompt_structure(self, mock_model):
        """Test that system prompt is sent with correct structure"""
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Result"
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        mock_progress = MagicMock()
        evaluate_startup_idea("Test", progress=mock_progress)
        
        # Verify start_chat was called with history
        call_args = mock_model.start_chat.call_args
        assert 'history' in call_args[1]
        history = call_args[1]['history']
        assert len(history) == 1
        assert history[0]['role'] == 'user'
        assert 'Feasibility' in history[0]['parts'][0]


class TestHelperFunctions:
    """Tests for helper functions"""
    
    def test_clear_inputs(self):
        """Test that clear_inputs returns empty strings"""
        result = clear_inputs()
        assert result == ("", "")
    
    def test_load_example(self):
        """Test that load_example returns the example text"""
        example_text = "Test example startup idea"
        result = load_example(example_text)
        assert result == example_text
    
    def test_examples_list_exists(self):
        """Test that examples list is properly defined"""
        assert isinstance(examples, list)
        assert len(examples) > 0
        assert all(isinstance(ex, str) for ex in examples)
    
    def test_examples_content(self):
        """Test that examples contain valid startup ideas"""
        assert len(examples) == 4
        for example in examples:
            assert len(example) > 20  # Each example should be descriptive
            assert example[0].isupper()  # Should start with capital letter


class TestGradioInterface:
    """Tests for Gradio interface components"""
    
    @patch("app.demo")
    def test_gradio_blocks_initialization(self, mock_demo):
        """Test that Gradio interface can be initialized"""
        # This test verifies the module loads without errors
        import app
        assert hasattr(app, 'demo')
    
    def test_custom_css_defined(self):
        """Test that custom CSS is defined"""
        from app import custom_css
        assert isinstance(custom_css, str)
        assert len(custom_css) > 0
        assert '.gradio-container' in custom_css


class TestIntegration:
    """Integration tests"""
    
    @patch("app.model")
    @patch("app.time.sleep")
    def test_full_evaluation_flow(self, mock_sleep, mock_model):
        """Test complete evaluation flow from input to output"""
        # Setup
        mock_convo = MagicMock()
        mock_response = MagicMock()
        full_response = """
        ## 1. Feasibility 🔧
        - Technically feasible
        
        ## 2. Market Potential 📈
        - Large market
        
        ## 3. Build Strategy 🗺️
        - MVP first
        
        ## 4. Cost & Team 💰
        - $50k budget
        
        ## 5. Improvements & Risks ⚠️
        - Consider regulations
        """
        mock_response.text = full_response
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        # Execute
        mock_progress = MagicMock()
        result = evaluate_startup_idea(
            "A blockchain-based supply chain tracker",
            progress=mock_progress
        )
        
        # Verify
        assert "Feasibility" in result
        assert "Market Potential" in result
        assert "Build Strategy" in result
        assert "Cost & Team" in result
        assert "Risks" in result or "Improvements" in result
    
    @patch("app.genai.configure")
    def test_api_configuration(self, mock_configure):
        """Test that API is configured on module import"""
        # Reimport to trigger configuration
        import importlib
        import app
        importlib.reload(app)
        
        # Note: This test verifies the module structure
        # In production, API keys should be environment variables


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    @patch("app.model")
    def test_very_long_prompt(self, mock_model):
        """Test handling of very long prompts"""
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Evaluation"
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        long_prompt = "A" * 10000
        mock_progress = MagicMock()
        result = evaluate_startup_idea(long_prompt, progress=mock_progress)
        
        assert result == "Evaluation"
    
    @patch("app.model")
    def test_special_characters_in_prompt(self, mock_model):
        """Test handling of special characters"""
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Evaluation"
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        special_prompt = "Test with émojis 🚀 and spëcial çharacters"
        mock_progress = MagicMock()
        result = evaluate_startup_idea(special_prompt, progress=mock_progress)
        
        assert result == "Evaluation"
    
    @patch("app.model")
    def test_none_response_text(self, mock_model):
        """Test handling when response.text is None"""
        mock_convo = MagicMock()
        mock_response = MagicMock()
        mock_response.text = None
        mock_convo.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_convo
        
        mock_progress = MagicMock()
        result = evaluate_startup_idea("Test", progress=mock_progress)
        
        # Should handle None gracefully
        assert result is None or isinstance(result, str)


# Fixtures
@pytest.fixture
def mock_progress():
    """Fixture for mocked progress tracker"""
    return MagicMock()


@pytest.fixture
def sample_startup_ideas():
    """Fixture providing sample startup ideas for testing"""
    return [
        "AI-powered fitness coach",
        "Blockchain supply chain tracker",
        "AR home design app",
        "Automated meal planning service"
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])