# Authentication Responses

This directory contains API responses related to authentication operations:

- **Login**: Token acquisition responses
- **Token Refresh**: Response data from token refresh operations
- **Logout**: Any logout-related responses

## Common Fields

Authentication responses typically contain:

- `access_token`: The JWT access token
- `token_type`: Usually "Bearer"
- `expires_in`: Token validity period in seconds
- `refresh_token`: Token used to obtain a new access token

## Example Structure

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IkYyNjZCQzA5RkE5...",
  "expires_in": 3600,
  "token_type": "Bearer",
  "refresh_token": "1a2b3c4d5e6f7g8h9i0j..."
}
```

## Usage in Code

```python
# Reference response format when handling authentication
def handle_auth_response(auth_response):
    token = auth_response.get("access_token")
    expires_in = auth_response.get("expires_in")
    # Calculate expiry time
    expiry_time = datetime.now() + timedelta(seconds=expires_in)
    # Store tokens securely
```
