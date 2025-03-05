# Markets Data Responses

This directory contains API responses related to betting markets and odds:

- **Match Markets**: Available betting markets for a match
- **Market Details**: Detailed information about a specific market
- **Odds**: Current and historical odds data
- **Market Changes**: Odds movement data

## Common Fields

Market responses typically contain:

- `marketId`: Unique identifier for the market
- `name`: Market name (e.g., "Match Result", "Over/Under 2.5 Goals")
- `status`: Market status (open, suspended, closed, etc.)
- `selections`: Array of betting selections
  - `selectionId`: Unique identifier for the selection
  - `name`: Selection name (e.g., "Home Win", "Over 2.5")
  - `odds`: Current odds for this selection
  - `status`: Selection status (active, suspended, etc.)

## Example Structure

```json
{
  "marketId": "12345",
  "name": "Match Result",
  "status": "OPEN",
  "selections": [
    {
      "selectionId": "12345-1",
      "name": "Home Win",
      "odds": 2.5,
      "status": "ACTIVE"
    },
    {
      "selectionId": "12345-2",
      "name": "Draw",
      "odds": 3.4,
      "status": "ACTIVE"
    },
    {
      "selectionId": "12345-3",
      "name": "Away Win",
      "odds": 2.9,
      "status": "ACTIVE"
    }
  ]
}
```

## Usage in Code

```python
# Reference response format when handling market data
def process_market_data(market):
    market_id = market.get("marketId")
    market_name = market.get("name")
    selections = market.get("selections", [])
    
    print(f"Market: {market_name} (ID: {market_id})")
    for selection in selections:
        name = selection.get("name")
        odds = selection.get("odds")
        print(f"  {name}: {odds}")
```
