# Betting Responses

This directory contains API responses related to bet placement and management:

- **Bet Placement**: Responses from bet placement attempts
- **Bet History**: User's historical betting data
- **Bet Details**: Detailed information about specific bets
- **Bet Settlement**: Information about settled bets

## Common Fields

Betting responses typically contain:

- `betId`: Unique identifier for the bet
- `status`: Bet status (pending, accepted, rejected, settled, etc.)
- `stake`: Amount wagered
- `potentialReturn`: Potential winnings including stake
- `betType`: Type of bet (single, multiple, etc.)
- `placedAt`: Timestamp when the bet was placed
- `selections`: Array of selections included in the bet
  - `selectionId`: Selection identifier
  - `marketId`: Market identifier
  - `matchId`: Match identifier
  - `odds`: Odds taken
  - `result`: Result of this selection (win, lose, void, etc.)

## Example Structure

```json
{
  "betId": "BET123456789",
  "status": "ACCEPTED",
  "stake": 50.00,
  "potentialReturn": 125.00,
  "betType": "SINGLE",
  "placedAt": "2025-03-05T13:45:23Z",
  "selections": [
    {
      "selectionId": "12345-1",
      "marketId": "12345",
      "matchId": "1234567",
      "matchName": "Manchester United vs Liverpool",
      "marketName": "Match Result",
      "selectionName": "Home Win",
      "odds": 2.5,
      "result": null
    }
  ]
}
```

## Bet Placement Request Example

```json
{
  "stake": 50.00,
  "betType": "SINGLE",
  "selections": [
    {
      "selectionId": "12345-1",
      "odds": 2.5
    }
  ]
}
```

## Usage in Code

```python
# Reference response format when handling bet data
def handle_bet_response(bet_response):
    bet_id = bet_response.get("betId")
    status = bet_response.get("status")
    stake = bet_response.get("stake")
    potential_return = bet_response.get("potentialReturn")
    
    print(f"Bet {bet_id} ({status})")
    print(f"Stake: {stake}, Potential Return: {potential_return}")
    
    for selection in bet_response.get("selections", []):
        match = selection.get("matchName")
        market = selection.get("marketName")
        pick = selection.get("selectionName")
        odds = selection.get("odds")
        
        print(f"  {match} - {market}: {pick} @ {odds}")
```
