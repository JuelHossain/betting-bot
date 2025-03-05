# SharpXch Betting Bot

An automated betting bot that interfaces with the SharpXch betting API to authenticate, collect match information, and place bets based on predefined strategies.

## Features

- **API Authentication**: Secure authentication with the SharpXch API
- **Profile Retrieval**: Fetch user account information and balance
- **Sports Data**: Retrieve sports and matches data
- **Betting Strategies**: Implement various betting strategies
- **Automated Betting**: Place bets automatically based on strategies

## Project Structure

```
betting-bot/
│
├── config/             # Configuration files
│   ├── betting_config.py  # Betting strategies configuration
│   └── logging_config.py  # Logging configuration
│
├── data/               # Data storage
│
├── logs/               # Log files
│
├── src/                # Source code
│   ├── api/            # API client modules
│   │   └── sharpxch_client.py  # SharpXch API client
│   │
│   ├── models/         # Data models
│   │   ├── api_models.py    # API response models
│   │   └── profile_model.py # User profile models
│   │
│   ├── strategies/     # Betting strategies
│   │
│   └── utils/          # Utility functions
│       ├── config.py        # Configuration utilities
│       ├── data_manager.py  # Data management utilities
│       └── logger.py        # Logging utilities
│
├── tests/              # Test suite
│   ├── api/            # API tests
│   └── integration/    # Integration tests
│
├── .env                # Environment variables (from .env.example)
├── main.py             # Main entry point
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/betting-bot.git
   cd betting-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Usage

**Run the betting bot**
```bash
python main.py
```

**Run the tests**
```bash
pytest
```

## Development

**Code formatting**
```bash
black .
```

**Run linter**
```bash
flake8
```

**Sort imports**
```bash
isort .
```

## License

MIT
