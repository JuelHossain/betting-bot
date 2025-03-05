"""
SharpXch API client for interacting with the betting service.
"""
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any

import requests
from requests.exceptions import RequestException

from ..utils.config import API_BASE_URL, API_USERNAME, API_PASSWORD, AUTH_ENDPOINT
from ..utils.logger import logger


class SharpXchClient:
    """
    Client for interacting with the SharpXch betting API.
    
    This client handles authentication, session management,
    and provides methods for retrieving user profile data.
    """
    
    def __init__(self, base_url: str = API_BASE_URL, username: str = API_USERNAME, 
                password: str = API_PASSWORD, auth_endpoint: str = AUTH_ENDPOINT,
                save_responses: bool = False):
        """
        Initialize the SharpXch API client.
        
        Args:
            base_url: Base URL for the API
            username: API username
            password: API password
            auth_endpoint: Authentication endpoint
            save_responses: Whether to save API responses to disk
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth_endpoint = auth_endpoint
        self.token = None
        self.token_expiry = None
        self.refresh_token = None
        self.session = requests.Session()
        self.save_responses = save_responses
        
        # Add default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BettingBot/1.0.0'
        })
        
        # Create response directories if saving is enabled
        if self.save_responses:
            self._ensure_response_directories()
        
        logger.info(f"Initialized SharpXch client with base URL: {base_url}")
    
    def _ensure_response_directories(self):
        """Ensure that the API response directories exist."""
        # Base directory for responses
        base_dir = Path(__file__).parent.parent.parent.parent / "data" / "api_responses"
        
        # Create subdirectories
        for subdir in ["auth", "profile", "sports", "markets", "bets"]:
            os.makedirs(base_dir / subdir, exist_ok=True)
    
    def _save_response(self, response_data: Dict[str, Any], category: str, status: str = "success"):
        """
        Save API response data to the appropriate directory.
        
        Args:
            response_data: The response data to save
            category: The category (auth, profile, sports, markets, bets)
            status: Response status (success or error)
        """
        if not self.save_responses:
            return
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Base directory for responses
        base_dir = Path(__file__).parent.parent.parent.parent / "data" / "api_responses"
        
        # Create filename
        filename = f"{category}_{status}_{timestamp}.json"
        
        # Full path
        full_path = base_dir / category / filename
        
        # Save response data
        with open(full_path, "w") as f:
            json.dump(response_data, f, indent=2)
        
        logger.debug(f"Saved {category} response to {full_path}")
    
    def _ensure_authenticated(self) -> bool:
        """
        Ensure that the client is authenticated with a valid token.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        # Check if token exists and is still valid (with 5 minute buffer)
        if (self.token is not None and self.token_expiry is not None and 
            datetime.now() < self.token_expiry - timedelta(minutes=5)):
            return True
        
        # Try to authenticate
        return self.login()
    
    def login(self) -> bool:
        """
        Authenticate with the API.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Prepare login request payload
            login_payload = {
                "username": self.username,
                "password": self.password
            }
            
            # Build the auth URL
            auth_url = f"{self.base_url}{self.auth_endpoint}"
            
            logger.debug(f"Attempting login to {auth_url}")
            
            # Make login request directly to the auth endpoint
            response = self.session.post(
                url=auth_url,
                json=login_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse response data
            response_data = response.json()
            
            # Save response if enabled
            self._save_response(response_data, "auth", "success")
            
            # Extract and store token
            if 'access_token' in response_data:
                self.token = response_data['access_token']
                
                # Store refresh token if available
                if 'refresh_token' in response_data:
                    self.refresh_token = response_data['refresh_token']
                
                # If expires_in is provided (in seconds), calculate expiry time
                if 'expires_in' in response_data:
                    expires_in = response_data['expires_in']
                    self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                else:
                    # Default expiry of 1 hour
                    self.token_expiry = datetime.now() + timedelta(hours=1)
                
                # Update session headers with the token
                self.session.headers.update({
                    'Authorization': f"Bearer {self.token}"
                })
                
                logger.info(f"Successfully logged in as {self.username}")
                logger.debug(f"Token expires at {self.token_expiry}")
                return True
            else:
                logger.error("Login failed: No access token in response")
                self.token = None
                self.token_expiry = None
                return False
        
        except Exception as e:
            logger.error(f"Login failed: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "auth", "error")
                except Exception:
                    pass
            
            self.token = None
            self.token_expiry = None
            return False
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get the user profile information.
        
        Returns:
            Dict: User profile information
        """
        # Use the specific URL for the profile endpoint
        profile_url = f"{self.base_url}/backoffice/api/v2/clients/profile"
        
        try:
            # Ensure we're authenticated
            if not self._ensure_authenticated():
                raise RequestException("Failed to authenticate with the API")
            
            # Set up headers with the token
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Make the request directly to the profile URL
            logger.debug(f"Fetching profile from {profile_url}")
            response = self.session.get(
                url=profile_url,
                headers=headers,
                timeout=30
            )
            
            # Log request details
            logger.debug(f"GET {profile_url} - Status: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            profile_data = response.json()
            
            # Save response if enabled
            self._save_response(profile_data, "profile", "success")
            
            logger.info(f"Retrieved user profile")
            return profile_data
        except Exception as e:
            logger.error(f"Failed to get profile: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "profile", "error")
                except Exception:
                    pass
            
            raise
    
    def get_sport_details(self) -> Dict[str, Any]:
        """
        Get sports list from the backoffice API.
        
        Returns:
            Dict: Sports list information
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise RequestException("Failed to authenticate with the API")
        
        # Use backoffice API for sports data instead of portal
        sports_url = f"{self.base_url}/backoffice/api/sports"
        
        try:
            # Set up headers with the token
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Make the request directly to the sports URL
            logger.debug(f"Fetching sports data from {sports_url}")
            response = self.session.get(
                url=sports_url,
                headers=headers,
                timeout=30
            )
            
            # Log request details
            logger.debug(f"GET {sports_url} - Status: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            sports_data = response.json()
            
            # Save response if enabled
            self._save_response(sports_data, "sports", "success")
            
            logger.info(f"Retrieved sports data")
            return sports_data
        except Exception as e:
            logger.error(f"Failed to get sports data: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "sports", "error")
                except Exception:
                    pass
            
            raise
    
    def get_matches(self, sport_id: int = None) -> Dict[str, Any]:
        """
        Get matches from the backoffice API.
        
        Args:
            sport_id: Optional ID of sport to filter matches
            
        Returns:
            Dict: Matches information
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise RequestException("Failed to authenticate with the API")
        
        # Build the matches URL
        matches_url = f"{self.base_url}/backoffice/api/matches"
        if sport_id:
            matches_url += f"?sportId={sport_id}"
        
        try:
            # Set up headers with the token
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Make the request
            logger.info(f"Fetching matches from {matches_url}")
            
            response = requests.get(
                url=matches_url,
                headers=headers,
                timeout=30
            )
            
            # Log request details
            logger.info(f"GET {matches_url} - Status: {response.status_code}")
            
            # Save the raw response for debugging
            with open("matches_raw_response.txt", "w", encoding="utf-8") as f:
                f.write(f"Status: {response.status_code}\n")
                f.write(f"Headers: {response.headers}\n\n")
                f.write(response.text)
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            try:
                # Parse the response as JSON
                matches_data = response.json()
                
                # Save the matches data to a file for inspection
                self._save_response(matches_data, "matches", "success")
                
                logger.info(f"Retrieved matches successfully")
                return matches_data
                
            except ValueError:
                # Handle case where response is not JSON
                logger.error(f"Response is not valid JSON")
                logger.debug(f"Response content: {response.text[:200]}...")
                raise RequestException("Invalid JSON response from matches endpoint")
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error with matches endpoint: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to get matches: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "matches", "error")
                except Exception:
                    pass
            
            raise
            
    def explore_available_endpoints(self) -> Dict[str, Any]:
        """
        Explore available endpoints from the backoffice API.
        
        This is a utility method to discover available API endpoints
        by checking common RESTful endpoint patterns.
        
        Returns:
            Dict: Mapping of endpoints to their response status
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise RequestException("Failed to authenticate with the API")
        
        # Common API endpoint patterns to check
        endpoint_patterns = [
            "/backoffice/api/sports",
            "/backoffice/api/matches",
            "/backoffice/api/events",
            "/backoffice/api/competitions",
            "/backoffice/api/markets",
            "/backoffice/api/odds",
            "/backoffice/api/bets",
            "/backoffice/api/account",
            "/backoffice/api/balance",
            "/backoffice/api/transactions",
            "/backoffice/api/user",
            "/backoffice/api/users/me",
            "/backoffice/api/profile"
        ]
        
        # Set up headers with the token
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
        
        # Results dictionary
        results = {}
        
        # Check each endpoint
        for endpoint in endpoint_patterns:
            url = f"{self.base_url}{endpoint}"
            
            try:
                logger.info(f"Checking endpoint: {url}")
                
                response = requests.get(
                    url=url,
                    headers=headers,
                    timeout=10  # Short timeout for exploration
                )
                
                status = response.status_code
                results[endpoint] = {
                    "status": status,
                    "available": 200 <= status < 300
                }
                
                # If successful, add sample data
                if 200 <= status < 300:
                    try:
                        data = response.json()
                        # Save only first few items if it's a list
                        if isinstance(data, list) and len(data) > 3:
                            sample = data[:3]
                        else:
                            sample = data
                        results[endpoint]["sample"] = sample
                    except ValueError:
                        results[endpoint]["sample"] = "Not JSON data"
                
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "available": False,
                    "error": str(e)
                }
        
        # Save results to file
        self._save_response(results, "endpoints", "success")
        
        logger.info(f"Endpoint exploration complete. Results saved to endpoints.json")
        return results
    
    def get_markets(self, match_id: str) -> Dict[str, Any]:
        """
        Get markets for a specific match.
        
        Args:
            match_id: Match ID to get markets for
            
        Returns:
            Dict: Markets data
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise RequestException("Failed to authenticate with the API")
        
        # Markets endpoint
        markets_url = f"{self.base_url}/backoffice/api/markets/{match_id}"
        
        try:
            # Set up headers with the token
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Make the request
            logger.debug(f"Fetching markets for match {match_id}")
            response = self.session.get(
                url=markets_url,
                headers=headers,
                timeout=30
            )
            
            # Log request details
            logger.debug(f"GET {markets_url} - Status: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            markets_data = response.json()
            
            # Save response if enabled
            self._save_response(markets_data, "markets", "success")
            
            logger.info(f"Retrieved markets data for match {match_id}")
            return markets_data
        except Exception as e:
            logger.error(f"Failed to get markets for match {match_id}: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "markets", "error")
                except Exception:
                    pass
            
            raise
    
    def place_bet(self, bet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Place a bet.
        
        Args:
            bet_data: Bet data including stake and selections
            
        Returns:
            Dict: Bet placement response
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise RequestException("Failed to authenticate with the API")
        
        # Bet placement endpoint
        bet_url = f"{self.base_url}/backoffice/api/bets"
        
        try:
            # Set up headers with the token
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Make the request
            logger.debug(f"Placing bet: {bet_data}")
            response = self.session.post(
                url=bet_url,
                json=bet_data,
                headers=headers,
                timeout=30
            )
            
            # Log request details
            logger.debug(f"POST {bet_url} - Status: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            bet_response = response.json()
            
            # Save response if enabled
            self._save_response(bet_response, "bets", "success")
            
            logger.info(f"Bet placed successfully")
            return bet_response
        except Exception as e:
            logger.error(f"Failed to place bet: {e}")
            
            # Save error response if enabled
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    self._save_response(error_data, "bets", "error")
                except Exception:
                    pass
            
            raise
