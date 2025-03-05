"""
Data models for the SharpXch API responses.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# Import our UserProfile model
from .profile_model import UserProfile


class LoginRequest(BaseModel):
    """Login request payload."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response from the API."""
    token: str
    expires_at: Optional[datetime] = None
    user_id: Optional[str] = None
    message: Optional[str] = None


class Match(BaseModel):
    """Model representing a sports match."""
    id: str
    sport: str
    competition: str
    home_team: str
    away_team: str
    start_time: datetime
    status: str
    score: Optional[str] = None
    markets: Optional[Dict[str, Any]] = None
    

class Market(BaseModel):
    """Model representing a betting market for a match."""
    id: str
    match_id: str
    name: str
    status: str
    selections: List['Selection']


class Selection(BaseModel):
    """Model representing a selection within a market."""
    id: str
    market_id: str
    name: str
    odds: float
    status: str
    result: Optional[str] = None


class Bet(BaseModel):
    """Model for placing a bet."""
    selection_id: str
    stake: float
    odds: float


class BetResponse(BaseModel):
    """Response after placing a bet."""
    id: str
    status: str
    selection_id: str
    match_id: str
    stake: float
    potential_return: float
    placed_at: datetime
    odds: float
    error: Optional[str] = None


class MatchesResponse(BaseModel):
    """Response containing a list of matches."""
    matches: List[Match]
    count: int
    page: int
    total_pages: int


class MarketsResponse(BaseModel):
    """Response containing markets for a match."""
    match_id: str
    markets: List[Market]


# Enable self-referencing for Selection class
Selection.update_forward_refs()
