"""
Utility functions and helpers for the stock sentiment analysis project.
"""

import re
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def extract_stock_symbols(text: str) -> List[str]:
    """
    Extract stock symbols from text (format: $SYMBOL).
    
    Args:
        text: Text to search for stock symbols
        
    Returns:
        List of stock symbols found
    """
    # Pattern to match stock symbols like $AAPL, $TSLA, etc.
    pattern = r'\$([A-Z]{1,5})'
    symbols = re.findall(pattern, text.upper())
    return list(set(symbols))  # Remove duplicates


def clean_text(text: str) -> str:
    """
    Clean text for sentiment analysis.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove mentions and hashtags for cleaner sentiment analysis
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def get_time_window(hours: int = 24) -> datetime:
    """
    Get datetime for time window analysis.
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        Datetime object for the cutoff time
    """
    return datetime.now() - timedelta(hours=hours)


def validate_api_credentials(credentials: Dict[str, Any]) -> bool:
    """
    Validate that API credentials are present.
    
    Args:
        credentials: Dictionary of API credentials
        
    Returns:
        True if all required credentials are present
    """
    required_keys = [key for key, value in credentials.items() if value is None]
    
    if required_keys:
        logger.warning(f"Missing API credentials: {required_keys}")
        return False
    
    return True


def calculate_sentiment_score(positive: float, negative: float, neutral: float) -> float:
    """
    Calculate a normalized sentiment score.
    
    Args:
        positive: Positive sentiment score
        negative: Negative sentiment score
        neutral: Neutral sentiment score
        
    Returns:
        Normalized sentiment score between -1 and 1
    """
    total = positive + negative + neutral
    if total == 0:
        return 0.0
    
    # Normalize to -1 to 1 scale
    return (positive - negative) / total


def setup_directories():
    """Create necessary directories if they don't exist."""
    import os
    
    directories = [
        'data/raw',
        'data/processed', 
        'data/results',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Create .gitkeep files for empty directories
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')


def format_stock_mention(symbol: str, mentions: int, sentiment: float) -> Dict[str, Any]:
    """
    Format stock mention data for consistent storage.
    
    Args:
        symbol: Stock symbol
        mentions: Number of mentions
        sentiment: Average sentiment score
        
    Returns:
        Formatted stock mention dictionary
    """
    return {
        'symbol': symbol.upper(),
        'mentions': mentions,
        'sentiment_score': round(sentiment, 4),
        'timestamp': datetime.now().isoformat()
    }
