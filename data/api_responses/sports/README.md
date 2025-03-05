# Sports Data Responses

This directory contains API responses related to sports and match information:

- **Sports List**: Available sports on the platform
- **Competitions**: Leagues and tournaments
- **Matches**: Upcoming and in-play match data
- **Match Details**: Detailed information for specific matches

## Common Fields

Sports data responses typically contain:

- **Sports List**: Sport ID, name, active status
- **Competitions**: Competition ID, name, country, sport ID
- **Matches**: 
  - Match ID
  - Home/away teams
  - Start time
  - Competition information
  - Current score (for in-play)
  - Match status

## Example Structure

```json
{
  "content": [
    {
      "id": "1234567",
      "homeTeam": "Manchester United",
      "awayTeam": "Liverpool",
      "startTime": "2025-03-10T15:00:00Z",
      "competition": "Premier League",
      "sportId": "1",
      "sportName": "Soccer",
      "status": "Scheduled"
    },
    {
      "id": "1234568",
      "homeTeam": "Real Madrid",
      "awayTeam": "Barcelona",
      "startTime": "2025-03-11T19:45:00Z",
      "competition": "La Liga",
      "sportId": "1",
      "sportName": "Soccer",
      "status": "Scheduled"
    }
  ],
  "totalPages": 25,
  "pageNumber": 1,
  "pageSize": 20
}
```

## Usage in Code

```python
# Reference response format when handling sports data
def handle_sports_data(sports_data):
    matches = sports_data.get("content", [])
    for match in matches:
        match_id = match.get("id")
        home_team = match.get("homeTeam")
        away_team = match.get("awayTeam")
        start_time = match.get("startTime")
        print(f"Match {match_id}: {home_team} vs {away_team} at {start_time}")
```
