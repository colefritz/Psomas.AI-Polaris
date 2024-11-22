import pytest
from unittest.mock import patch, AsyncMock
import os
import json


def pytest_addoption(parser):
    parser.addoption(
        "--use-keyvault-secrets",
        help='Get secrets from a keyvault instead of the environment.',
        action='store_true',
        default=False
    )


@pytest.fixture(scope="session")
def use_keyvault_secrets(request):
    return request.config.getoption("--use-keyvault-secrets")


@pytest.fixture(scope="function")
def mock_openai_response():
    """Mock the OpenAI API response"""
    async def mock_create(*args, **kwargs):
        return {
            "id": "mock-id",
            "object": "chat.completion",
            "created": 1677858242,
            "model": "gpt-4",
            "usage": {
                "prompt_tokens": 13,
                "completion_tokens": 7,
                "total_tokens": 20
            },
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a test response"
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }

    with patch('openai.AsyncClient') as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(side_effect=mock_create)
        yield mock_client.return_value.chat.completions.create


@pytest.fixture(scope="function")
def dotenv_template_params():
    """Provide template parameters for .env file generation"""
    return {
        # Azure OpenAI Settings
        "AZURE_OPENAI_MODEL": "gpt-4",
        "AZURE_OPENAI_DEPLOYMENT": "PsoGPT",
        "AZURE_OPENAI_KEY": "test-key-1234567890abcdef1234567890abcdef",
        "AZURE_OPENAI_ENDPOINT": "https://test-resource.openai.azure.com",
        "AZURE_OPENAI_RESOURCE": "test-resource",
        "AZURE_OPENAI_EMBEDDING_NAME": "text-embedding-ada-002",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": "embedding",
        "AZURE_OPENAI_SYSTEM_MESSAGE": "You are a test assistant.",
        "AZURE_OPENAI_TEMPERATURE": 0.3,
        "AZURE_OPENAI_TOP_P": 1,
        "AZURE_OPENAI_MAX_TOKENS": 2000,
        "AZURE_OPENAI_STOP_SEQUENCE": "",
        
        # Azure Search Settings
        "AZURE_SEARCH_SERVICE": "test-search",
        "AZURE_SEARCH_INDEX": "test-index",
        "AZURE_SEARCH_KEY": "test-search-key",
        "AZURE_SEARCH_QUERY": "What services does the company offer?",
        "AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG": "default",
        "AZURE_SEARCH_CONTENT_COLUMNS": "content",
        "AZURE_SEARCH_FILENAME_COLUMN": "filename",
        "AZURE_SEARCH_TITLE_COLUMN": "title",
        "AZURE_SEARCH_URL_COLUMN": "url",
        "AZURE_SEARCH_VECTOR_COLUMNS": "contentVector",
        "AZURE_SEARCH_TOP_K": 5,
        "AZURE_SEARCH_ENABLE_IN_DOMAIN": True,
        
        # Elasticsearch Settings
        "ELASTICSEARCH_ENDPOINT": "https://test-elastic.com",
        "ELASTICSEARCH_ENCODED_API_KEY": "test-elastic-key",
        "ELASTICSEARCH_INDEX": "test-index",
        "ELASTICSEARCH_QUERY": "What products are available?",
        "ELASTICSEARCH_CONTENT_COLUMNS": "text",
        "ELASTICSEARCH_VECTOR_COLUMNS": "text_embedding.predicted_value",
        
        # Cosmos DB Settings
        "AZURE_COSMOSDB_ACCOUNT": "test-cosmos",
        "AZURE_COSMOSDB_DATABASE": "test-db",
        "AZURE_COSMOSDB_CONTAINER": "test-container",
        "AZURE_COSMOSDB_ACCOUNT_KEY": "test-cosmos-key",
        "AZURE_COSMOSDB_ENABLE_FEEDBACK": True,
        
        # UI Settings
        "UI_TITLE": "Test Chat",
        "UI_LOGO": "test-logo.png",
        "UI_CHAT_TITLE": "Ask me anything",
        "UI_CHAT_DESCRIPTION": "This is a test chat interface",
        "UI_SHOW_SHARE_BUTTON": True,
        
        # General Settings
        "DATASOURCE_TYPE": "AzureCognitiveSearch",
        "AUTH_ENABLED": True,
        "FEEDBACK_ENABLED": True
    }


@pytest.fixture(scope="function")
def mock_chat_history_settings(monkeypatch):
    """Mock chat history settings"""
    chat_history_settings = {
        "AZURE_COSMOSDB_DATABASE": "test_db",
        "AZURE_COSMOSDB_ACCOUNT": "test_account",
        "AZURE_COSMOSDB_CONVERSATIONS_CONTAINER": "test_container",
        "AZURE_COSMOSDB_ACCOUNT_KEY": "test_key",
        "AZURE_COSMOSDB_ENABLE_FEEDBACK": True
    }
    
    for key, value in chat_history_settings.items():
        monkeypatch.setenv(key, str(value))
    
    return chat_history_settings


@pytest.fixture(autouse=True)
def mock_cosmos_client():
    """Mock the Cosmos DB client"""
    with patch('azure.cosmos.CosmosClient') as mock_client:
        mock_client.return_value.get_database_client.return_value.get_container_client.return_value.upsert_item = AsyncMock()
        yield mock_client


@pytest.fixture(scope="function")
def mock_search_client():
    """Mock the Azure Search client"""
    with patch('azure.search.documents.SearchClient') as mock_client:
        mock_client.return_value.search = AsyncMock(return_value=[
            {
                "content": "Test content",
                "title": "Test document",
                "url": "http://test.com",
                "filename": "test.pdf"
            }
        ])
        yield mock_client


@pytest.fixture(scope="function")
def mock_elasticsearch_client():
    """Mock the Elasticsearch client"""
    with patch('elasticsearch.AsyncElasticsearch') as mock_client:
        mock_client.return_value.search = AsyncMock(return_value={
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "content": "Test content",
                            "title": "Test document",
                            "url": "http://test.com"
                        }
                    }
                ]
            }
        })
        yield mock_client


@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment variables after each test"""
    yield
    # List of prefixes to clean up
    prefixes = [
        "AZURE_OPENAI_",
        "AZURE_SEARCH_",
        "ELASTICSEARCH_",
        "AZURE_COSMOSDB_",
        "UI_"
    ]
    
    for key in list(os.environ.keys()):
        for prefix in prefixes:
            if key.startswith(prefix):
                os.environ.pop(key, None)


@pytest.fixture(scope="function")
def mock_env(dotenv_template_params, monkeypatch):
    """Set up environment variables for testing"""
    for key, value in dotenv_template_params.items():
        monkeypatch.setenv(key, str(value))
    return dotenv_template_params