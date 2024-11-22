# tests/test_azure_openai.py
import pytest
from pydantic import ValidationError
from backend.settings import _AzureOpenAISettings

def test_azure_openai_missing_required_fields(monkeypatch):
    """Test that appropriate errors are raised when required fields are missing"""
    # Clear required environment variables
    monkeypatch.delenv("AZURE_OPENAI_MODEL", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_RESOURCE", raising=False)

    with pytest.raises(ValidationError) as exc_info:
        _AzureOpenAISettings()
    
    assert "field required" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_azure_openai_chat_completion(test_app, mock_openai_response):
    """Test chat completion with mocked response"""
    test_message = "Hello, who are you?"
    test_client = test_app.test_client()
    
    response = await test_client.post("/conversation", json={
        "messages": [{"role": "user", "content": test_message}]
    })
    
    assert response.status_code == 200
    response_data = await response.get_json()
    assert "content" in response_data
    
    # Verify mock was called with correct parameters
    mock_openai_response.assert_called_once()
    call_args = mock_openai_response.call_args[1]
    assert call_args["model"] == "gpt-4"
    assert call_args["messages"][0]["content"] == test_message