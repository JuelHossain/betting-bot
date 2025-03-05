# SharpXch Betting Bot - Project Context

This document serves as a reference for Cascade AI to understand the context, structure, and rules of this project across different chat sessions.

## Project Overview

This is a betting bot that interfaces with the SharpXch betting API to:
- Authenticate with the betting platform
- Collect match and market information
- Place bets based on predefined strategies
- Manage betting history and performance

The project has been refactored to follow modern Python practices, with improved organization, error handling, and test coverage.

## Project Structure

```
betting-bot/
├── config/                  # Configuration files
│   ├── betting_config.py    # Betting strategy configuration
│   └── logging_config.py    # Logging configuration
├── data/                    # Data storage
│   ├── api_responses/       # Stored API responses
│   │   ├── auth/            # Authentication responses
│   │   ├── bets/            # Betting-related responses
│   │   ├── markets/         # Market information
│   │   ├── profile/         # User profile data
│   │   └── sports/          # Sports and match data
├── logs/                    # Log files directory
├── src/                     # Source code
│   ├── api/                 # API client code
│   │   └── sharpxch_client.py  # SharpXch API client
│   ├── models/              # Data models
│   │   ├── api_models.py    # API response models
│   │   └── profile_model.py # User profile model
│   ├── strategies/          # Betting strategies
│   │   └── value_betting.py # Value betting strategy
│   └── utils/               # Utility modules
│       ├── config.py        # Configuration utilities
│       ├── data_manager.py  # Data management utilities
│       ├── logger.py        # Logging utilities
│       └── sequence_handler.py # Sequence handling
├── tests/                   # Test suite
│   ├── api/                 # API tests
│   │   └── test_sharpxch_api.py
│   ├── integration/         # Integration tests
│   │   └── test_end_to_end.py
│   └── conftest.py          # Shared test fixtures
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Key Components

### API Client (src/api/sharpxch_client.py)
- Handles authentication with the SharpXch API
- Makes API calls to get sports, markets, and place bets
- Saves API responses to disk for analysis and debugging
- Implements error handling and logging

### Configuration (config/)
- `betting_config.py`: Configuration for betting strategies
- `logging_config.py`: Logging configuration

### Data Storage (data/)
- Organized storage of API responses for analysis and debugging
- Each API endpoint has its own directory with README

### Testing (tests/)
- Comprehensive test suite using pytest
- API tests for individual endpoints
- Integration tests for end-to-end workflows
- Shared fixtures in conftest.py

## Work Completed

1. **Project Refactoring**
   - Reorganized directory structure
   - Removed redundant and duplicate files
   - Created modern, modular architecture

2. **API Client Improvements**
   - Added response saving functionality
   - Improved error handling
   - Added new methods for different endpoints

3. **Documentation**
   - Added comprehensive README files
   - Improved inline code documentation
   - Created directory structure documentation

4. **Testing**
   - Created pytest-based test infrastructure
   - Implemented skip markers for tests requiring special permissions
   - Added test fixtures

5. **GitHub Repository**
   - Created a public GitHub repository
   - Pushed all code to the repository
   - URL: https://github.com/JuelHossain/betting-bot

## Rules and Conventions

### Code Style
- Use latest versions of all technologies
- Organize code in a modular, maintainable manner
- Follow PEP 8 style guide for Python code
- Use proper naming conventions:
  - snake_case for variables, functions, methods, modules
  - CamelCase for classes
  - UPPER_CASE for constants
- Divide code into small, focused files rather than large monolithic ones
- Always add comments to explain complex logic or design decisions

### Variable Naming
- Use descriptive, meaningful variable names
- Avoid single-letter variables except in simple loops
- Use plural names for collections (lists, dicts)

### Function Design
- Functions should have a single responsibility
- Use descriptive function and method names
- Document parameters and return values
- Keep functions relatively short and focused

### Testing
- Write tests for all new functionality
- Use descriptive test names
- Include assertions with clear error messages
- Organize tests by module/feature

### Logging
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Include contextual information in log messages
- Use structured logging where appropriate

## Environment Setup

Required environment variables:
- `API_BASE_URL`: SharpXch API base URL
- `AUTH_ENDPOINT`: Authentication endpoint
- `API_USERNAME`: API username
- `API_PASSWORD`: API password

## TODOs and Future Work

1. Complete betting strategy implementation
2. Add more comprehensive error handling
3. Implement more advanced logging and monitoring
4. Create more detailed documentation
5. Expand test coverage
6. Implement more sophisticated authentication mechanisms

## Notes for Cascade AI

When continuing work on this project:
1. Familiarize yourself with the current structure before making changes
2. Maintain the modular organization
3. Follow the coding conventions established in the project
4. Continue to document new functionality
5. Add tests for new features
6. Ensure all environment variables are documented

**This file is for Cascade AI reference only and should be updated as the project evolves.**
