"""
End-to-end integration tests for the SharpXch betting bot.

These tests verify the complete workflow from authentication 
to data retrieval and bet placement.
"""
import sys
import json
import pytest
from pathlib import Path
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.sharpxch_client import SharpXchClient
from src.utils.config import API_BASE_URL, API_USERNAME, API_PASSWORD, AUTH_ENDPOINT


class TestEndToEndWorkflow:
    """End-to-end integration tests for the betting bot workflow."""
    
    @pytest.fixture
    def client(self):
        """Create a SharpXch client instance for testing."""
        return SharpXchClient(
            base_url=API_BASE_URL,
            username=API_USERNAME,
            password=API_PASSWORD,
            auth_endpoint=AUTH_ENDPOINT
        )
    
    def test_auth_and_profile_sequence(self, client):
        """Test the authentication and profile retrieval sequence."""
        # 1. Authenticate
        login_success = client.login()
        assert login_success, "Authentication failed"
        
        # 2. Get profile
        try:
            profile = client.get_profile()
            assert profile is not None, "Failed to retrieve profile"
            
            # Check profile data
            assert "username" in profile, "Username not in profile"
            assert "availableToBet" in profile, "Available balance not in profile"
        except Exception as e:
            pytest.fail(f"Profile retrieval failed: {e}")
    
    @pytest.mark.skip(reason="API may require special permissions")
    def test_sports_data_workflow(self, client):
        """Test the sports data retrieval workflow."""
        # 1. Authenticate
        login_success = client.login()
        assert login_success, "Authentication failed"
        
        # 2. Get sports details
        try:
            sport_details = client.get_sport_details()
            assert sport_details is not None, "Failed to retrieve sport details"
        except Exception as e:
            pytest.fail(f"Sport details retrieval failed: {e}")
    
    @pytest.mark.skip(reason="Betting functionality not yet implemented")
    def test_betting_workflow(self, client):
        """Test the complete betting workflow."""
        # This test will be implemented when betting functionality is added
        pass


if __name__ == "__main__":
    """Run tests directly if needed."""
    pytest.main(["-v", __file__])
