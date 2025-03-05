# API Responses

This directory contains organized storage for API responses captured from the SharpXch API.
These responses are useful for:

- **Testing**: Validate code against known API responses
- **Debugging**: Troubleshoot issues by comparing current vs. expected responses
- **Development**: Understand API structure without making actual API calls
- **Documentation**: Provide examples of API responses

## Directory Structure

- **auth/**: Authentication-related responses (login, token refresh)
- **profile/**: User profile and account information responses
- **sports/**: Sports, competitions, and match data responses
- **markets/**: Market and odds data for matches
- **bets/**: Betting-related responses (bet placement, bet history)

## Naming Convention

Files should follow this naming convention:
```
{endpoint}_[success|error]_[YYYYMMDD_HHMMSS].json
```

Examples:
- `auth_success_20250305_134159.json`
- `profile_error_20250305_134215.json`
- `sports_success_20250305_134230.json`

## Response Storage Utility

The API client automatically stores responses in these directories when the
`save_responses` flag is enabled in the client configuration.

### Example Usage

```python
from src.api.sharpxch_client import SharpXchClient

# Enable response saving
client = SharpXchClient(save_responses=True)

# Responses will be automatically saved in the appropriate directories
client.login()  # Saves to auth/
client.get_profile()  # Saves to profile/
client.get_sport_details()  # Saves to sports/
```
