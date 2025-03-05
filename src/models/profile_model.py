"""
Models for user profiles from the SharpXch API.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """
    User profile model for the SharpXch API.
    
    This model represents the user profile data returned from the 
    /backoffice/api/v2/clients/profile endpoint.
    """
    email: Optional[str] = None
    username: str
    first_name: str = Field(default="", alias="firstName")
    last_name: str = Field(default="", alias="lastName")
    currency: List[str]
    available_to_bet: float = Field(alias="availableToBet")
    exposure: float
    joined_date: datetime = Field(alias="joinedDate")
    mfa_enabled: bool = Field(alias="mfaEnabled")
    
    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        arbitrary_types_allowed = True
        
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    @property
    def primary_currency(self) -> Optional[str]:
        """Get the user's primary currency."""
        if self.currency and len(self.currency) > 0:
            return self.currency[0]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return self.model_dump(by_alias=False)
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create a UserProfile instance from the API response."""
        return cls.model_validate(data)
