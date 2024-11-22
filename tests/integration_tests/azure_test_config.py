import pytest
import os

@pytest.fixture(scope="function")
def azure_openai_env():
    """Setup test environment variables for Azure OpenAI"""
    original_env = {}
    test_vars = {
        'AZURE_OPENAI_KEY': 'test-key-1234567890abcdef1234567890abcdef',
        'AZURE_OPENAI_ENDPOINT': 'https://test-resource.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'test-deployment',
        'AZURE_OPENAI_MODEL': 'gpt-4'
    }
    
    # Save original state
    for var in test_vars:
        original_env[var] = os.environ.get(var)
        
    # Set test values
    for var, value in test_vars.items():
        os.environ[var] = value
        
    yield test_vars
    
    # Restore original state
    for var, value in original_env.items():
        if value is None:
            os.environ.pop(var, None)
        else:
            os.environ[var] = value