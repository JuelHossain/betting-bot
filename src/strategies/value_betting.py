"""
Value betting strategy module.

This strategy identifies value bets by comparing our calculated probability
with the implied probability from the bookmaker's odds.
"""
from typing import Dict, List, Tuple, Any, Optional
import logging

from ..models.api_models import Match, Market, Selection
from ..utils.config import MAX_STAKE, MIN_ODDS


class ValueBettingStrategy:
    """
    Value betting strategy implementation.
    
    This strategy tries to find bets where our estimated probability
    is higher than the implied probability from the odds.
    """
    
    def __init__(self, min_value: float = 0.05, confidence_threshold: float = 0.7):
        """
        Initialize the value betting strategy.
        
        Args:
            min_value: Minimum edge/value required (e.g., 0.05 means 5%)
            confidence_threshold: Minimum confidence in our probability estimate
        """
        self.min_value = min_value
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)
    
    def calculate_value(self, our_probability: float, bookmaker_odds: float) -> float:
        """
        Calculate the value/edge for a bet.
        
        Args:
            our_probability: Our estimated probability of the outcome
            bookmaker_odds: The bookmaker's odds for the outcome
            
        Returns:
            float: The calculated value/edge
        """
        # Implied probability from the odds
        implied_probability = 1 / bookmaker_odds
        
        # Calculate the value/edge
        value = our_probability - implied_probability
        
        return value
    
    def analyze_selection(self, selection: Selection, our_probability: float) -> Dict[str, Any]:
        """
        Analyze a selection for value betting.
        
        Args:
            selection: The betting selection
            our_probability: Our estimated probability
            
        Returns:
            Dict: Analysis results
        """
        # Calculate value
        value = self.calculate_value(our_probability, selection.odds)
        
        # Determine if this is a value bet
        is_value_bet = (
            value >= self.min_value and
            selection.odds >= MIN_ODDS and
            our_probability >= self.confidence_threshold
        )
        
        # Calculate recommended stake if it's a value bet
        stake = MAX_STAKE * value * 10 if is_value_bet else 0
        
        return {
            "selection": selection,
            "our_probability": our_probability,
            "implied_probability": 1 / selection.odds,
            "value": value,
            "is_value_bet": is_value_bet,
            "recommended_stake": min(stake, MAX_STAKE)
        }
    
    def find_value_bets(self, match: Match, market: Market, 
                        probability_estimates: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Find value bets in a market.
        
        Args:
            match: The match data
            market: The betting market
            probability_estimates: Our estimated probabilities for each selection
            
        Returns:
            List[Dict]: List of value betting opportunities
        """
        value_bets = []
        
        for selection in market.selections:
            # Skip if we don't have a probability estimate for this selection
            if selection.name not in probability_estimates:
                continue
            
            our_probability = probability_estimates[selection.name]
            
            # Analyze the selection
            analysis = self.analyze_selection(selection, our_probability)
            
            # If it's a value bet, add it to our list
            if analysis["is_value_bet"]:
                self.logger.info(
                    f"Found value bet: {match.home_team} vs {match.away_team} - "
                    f"{market.name} - {selection.name} - "
                    f"Odds: {selection.odds:.2f}, Value: {analysis['value']:.2%}"
                )
                value_bets.append(analysis)
        
        return value_bets
