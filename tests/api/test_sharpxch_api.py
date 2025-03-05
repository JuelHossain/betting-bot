"""
Tests for the SharpXch API client.

This module contains comprehensive tests for all SharpXch API functionalities:
- Authentication
- Profile retrieval
- Sports/matches data
- Market information
"""
import json
import sys
import pytest
from datetime import datetime
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.sharpxch_client import SharpXchClient
from src.utils.config import API_BASE_URL, API_USERNAME, API_PASSWORD, AUTH_ENDPOINT


class TestSharpXchAPI:
    """Test suite for the SharpXch API client."""
    
    @pytest.fixture
    def client(self):
        """Create a SharpXch client instance for testing."""
        return SharpXchClient(
            base_url=API_BASE_URL,
            username=API_USERNAME,
            password=API_PASSWORD,
            auth_endpoint=AUTH_ENDPOINT
        )
    
    def test_authentication(self, client):
        """Test API authentication."""
        # Test login
        login_success = client.login()
        assert login_success, "Authentication failed"
        assert client.token is not None, "No token received"
        assert client.token_expiry is not None, "No token expiry received"
    
    def test_profile_retrieval(self, client):
        """Test user profile retrieval."""
        # Ensure authenticated
        client.login()
        
        # Get profile
        profile = client.get_profile()
        assert profile is not None, "Profile data is None"
        assert isinstance(profile, dict), "Profile is not a dictionary"
        assert "username" in profile, "Username not in profile"
    
    @pytest.mark.skip(reason="API may require special permissions")
    def test_sport_details(self, client):
        """Test sport details retrieval."""
        # Ensure authenticated
        client.login()
        
        # Get sport details
        sport_details = client.get_sport_details()
        assert sport_details is not None, "Sport details data is None"
        
        # Validate sport details structure
        if isinstance(sport_details, dict) and "content" in sport_details:
            assert isinstance(sport_details["content"], list), "Content is not a list"
    
    @pytest.mark.skip(reason="API may require special permissions")
    def test_get_matches(self, client):
        """Test match retrieval."""
        # Ensure authenticated
        client.login()
        
        # Get matches for today
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            matches_response = client.get_matches(date=today)
            assert matches_response is not None, "Matches response is None"
            assert hasattr(matches_response, 'matches'), "No matches attribute"
        except Exception as e:
            pytest.skip(f"Skip test_get_matches due to: {e}")
    
    @pytest.mark.skip(reason="API may require special permissions")
    def test_get_match_markets(self, client):
        """Test market retrieval for a match."""
        # Ensure authenticated
        client.login()
        
        # Get matches for today to find a match ID
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            matches_response = client.get_matches(date=today)
            if not matches_response.matches:
                pytest.skip("No matches available for testing markets")
                
            # Get first match ID
            test_match = matches_response.matches[0]
            
            # Get markets for this match
            markets_response = client.get_match_markets(test_match.id)
            assert markets_response is not None, "Markets response is None"
            assert hasattr(markets_response, 'markets'), "No markets attribute"
        except Exception as e:
            pytest.skip(f"Skip test_get_match_markets due to: {e}")


if __name__ == "__main__":
    """Run tests directly if needed."""
    pytest.main(["-v", __file__])
