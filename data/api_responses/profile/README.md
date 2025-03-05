# Profile Responses

This directory contains API responses related to user profile information:

- **User Profile**: Basic account information
- **Account Balance**: Financial account status
- **Account Limits**: Betting limits and restrictions
- **User Settings**: User preferences and settings

## Common Fields

Profile responses typically contain:

- `username`: The account username
- `availableToBet`: Current available balance
- `currency`: Account currency (array)
- `joinedDate`: Account creation date
- `firstName`, `lastName`: User's name (if provided)
- `email`: User's email address
- `phone`: Contact phone number
- `address`: User's address information

## Example Structure

```json
{
  "username": "jrrahman01",
  "availableToBet": 1000.00,
  "currency": ["USD"],
  "joinedDate": "2024-01-15T08:30:45.123Z",
  "firstName": "John",
  "lastName": "Rahman",
  "email": "jr@example.com"
}
```

## Usage in Code

```python
# Reference response format when handling profile data
def handle_profile_response(profile):
    username = profile.get("username", "Unknown")
    balance = profile.get("availableToBet", 0.0)
    currency = profile.get("currency", [""])[0] or "USD"
    
    print(f"User {username} has {balance} {currency} available")
```
