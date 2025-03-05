"""
Pytest configuration file with shared fixtures.
"""
import sys
import pytest
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.sharpxch_client import SharpXchClient
from src.utils.config import API_BASE_URL, API_USERNAME, API_PASSWORD, AUTH_ENDPOINT


@pytest.fixture(scope="session")
def api_client():
    """Create a SharpXch client instance for testing."""
    return SharpXchClient(
        base_url=API_BASE_URL,
        username=API_USERNAME,
        password=API_PASSWORD,
        auth_endpoint=AUTH_ENDPOINT
    )


@pytest.fixture(scope="session")
def authenticated_client(api_client):
    """Create a pre-authenticated API client."""
    api_client.login()
    return api_client
