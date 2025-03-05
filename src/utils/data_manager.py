"""
Data manager for storing and retrieving match information.
"""
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ..models.api_models import Match, Market, Selection
from ..utils.config import ROOT_DIR
from ..utils.logger import logger


class DataManager:
    """
    Data manager for storing and retrieving match and betting data.
    
    This class handles:
    - Storing match data in JSON format
    - Converting data to CSV for analysis
    - Managing data directories and files
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data manager.
        
        Args:
            data_dir: Directory for storing data files
        """
        self.data_dir = ROOT_DIR / data_dir
        self.matches_dir = self.data_dir / "matches"
        self.markets_dir = self.data_dir / "markets"
        self.bets_dir = self.data_dir / "bets"
        
        # Ensure directories exist
        self._ensure_dirs_exist()
        
        logger.info(f"Initialized DataManager with data directory: {self.data_dir}")
    
    def _ensure_dirs_exist(self):
        """Ensure that all required directories exist."""
        for directory in [self.data_dir, self.matches_dir, self.markets_dir, self.bets_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _get_date_path(self, date: Optional[datetime] = None) -> Path:
        """
        Get path for a specific date.
        
        Args:
            date: Date to get path for, defaults to today
            
        Returns:
            Path: Path for the date
        """
        if date is None:
            date = datetime.now()
        
        return Path(date.strftime("%Y-%m-%d"))
    
    def save_matches(self, matches: List[Match], date: Optional[datetime] = None):
        """
        Save matches to JSON file.
        
        Args:
            matches: List of matches to save
            date: Date for organizing files, defaults to today
        """
        date_path = self._get_date_path(date)
        file_path = self.matches_dir / date_path / "matches.json"
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert matches to dict
        matches_data = [match.dict() for match in matches]
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(matches_data, f, indent=2, default=str)
        
        logger.info(f"Saved {len(matches)} matches to {file_path}")
    
    def save_match_markets(self, match_id: str, markets: List[Market], date: Optional[datetime] = None):
        """
        Save markets for a match to JSON file.
        
        Args:
            match_id: ID of the match
            markets: List of markets to save
            date: Date for organizing files, defaults to today
        """
        date_path = self._get_date_path(date)
        file_path = self.markets_dir / date_path / f"{match_id}.json"
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert markets to dict
        markets_data = [market.dict() for market in markets]
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(markets_data, f, indent=2, default=str)
        
        logger.info(f"Saved {len(markets)} markets for match {match_id} to {file_path}")
    
    def load_matches(self, date: Optional[datetime] = None) -> List[Dict]:
        """
        Load matches from JSON file.
        
        Args:
            date: Date to load matches for, defaults to today
            
        Returns:
            List[Dict]: List of match data
        """
        date_path = self._get_date_path(date)
        file_path = self.matches_dir / date_path / "matches.json"
        
        if not file_path.exists():
            logger.warning(f"No matches found for {date_path}")
            return []
        
        # Load from file
        with open(file_path, 'r') as f:
            matches_data = json.load(f)
        
        logger.info(f"Loaded {len(matches_data)} matches from {file_path}")
        return matches_data
    
    def load_match_markets(self, match_id: str, date: Optional[datetime] = None) -> List[Dict]:
        """
        Load markets for a match from JSON file.
        
        Args:
            match_id: ID of the match
            date: Date to load markets for, defaults to today
            
        Returns:
            List[Dict]: List of market data
        """
        date_path = self._get_date_path(date)
        file_path = self.markets_dir / date_path / f"{match_id}.json"
        
        if not file_path.exists():
            logger.warning(f"No markets found for match {match_id} on {date_path}")
            return []
        
        # Load from file
        with open(file_path, 'r') as f:
            markets_data = json.load(f)
        
        logger.info(f"Loaded {len(markets_data)} markets for match {match_id} from {file_path}")
        return markets_data
    
    def export_matches_to_csv(self, date: Optional[datetime] = None) -> str:
        """
        Export matches to CSV file for analysis.
        
        Args:
            date: Date to export matches for, defaults to today
            
        Returns:
            str: Path to the CSV file
        """
        date_path = self._get_date_path(date)
        matches_data = self.load_matches(date)
        
        if not matches_data:
            logger.warning(f"No matches to export for {date_path}")
            return ""
        
        # Convert to DataFrame
        df = pd.DataFrame(matches_data)
        
        # Export to CSV
        csv_path = self.data_dir / "exports" / date_path / "matches.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Exported {len(matches_data)} matches to {csv_path}")
        return str(csv_path)
    
    def save_bet(self, bet_data: Dict, date: Optional[datetime] = None):
        """
        Save bet information to JSON file.
        
        Args:
            bet_data: Bet data to save
            date: Date for organizing files, defaults to today
        """
        date_path = self._get_date_path(date)
        bets_dir = self.bets_dir / date_path
        bets_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = bets_dir / f"bet_{bet_data.get('id', timestamp)}.json"
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(bet_data, f, indent=2, default=str)
        
        logger.info(f"Saved bet information to {file_path}")
    
    def load_bets(self, date: Optional[datetime] = None) -> List[Dict]:
        """
        Load all bets for a specific date.
        
        Args:
            date: Date to load bets for, defaults to today
            
        Returns:
            List[Dict]: List of bet data
        """
        date_path = self._get_date_path(date)
        bets_dir = self.bets_dir / date_path
        
        if not bets_dir.exists():
            logger.warning(f"No bets found for {date_path}")
            return []
        
        bets_data = []
        for file_path in bets_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                bet_data = json.load(f)
                bets_data.append(bet_data)
        
        logger.info(f"Loaded {len(bets_data)} bets from {bets_dir}")
        return bets_data
