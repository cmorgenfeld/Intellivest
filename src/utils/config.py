"""
Configuration management for the stock sentiment analysis project.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration management class."""
    
    def __init__(self):
        self.config_path = Path("config/settings.yaml")
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Return default configuration if file not found
            return self._default_config()
    
    def _default_config(self):
        """Default configuration."""
        return {
            'reddit': {
                'subreddit': 'wallstreetbets',
                'sort_by': 'hot',
                'limit': 100,
                'time_filter': 'day'
            },
            'twitter': {
                'search_terms': ['$SPY', '$AAPL', '$TSLA', '$NVDA'],
                'max_tweets': 500,
                'include_retweets': False
            },
            'sentiment': {
                'model': 'vader',
                'threshold': 0.1,
                'language': 'en'
            },
            'analysis': {
                'window_hours': 24,
                'min_mentions': 5,
                'weight_reddit': 0.6,
                'weight_twitter': 0.4
            }
        }
    
    @property
    def reddit_config(self):
        """Get Reddit configuration."""
        return self.config.get('reddit', {})
    
    @property
    def twitter_config(self):
        """Get Twitter configuration."""
        return self.config.get('twitter', {})
    
    @property
    def sentiment_config(self):
        """Get sentiment analysis configuration."""
        return self.config.get('sentiment', {})
    
    @property
    def analysis_config(self):
        """Get analysis configuration."""
        return self.config.get('analysis', {})
    
    @property
    def reddit_credentials(self):
        """Get Reddit API credentials from environment."""
        return {
            'client_id': os.getenv('REDDIT_CLIENT_ID'),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
            'user_agent': os.getenv('REDDIT_USER_AGENT', 'StockSentimentBot/1.0')
        }
    
    @property
    def twitter_credentials(self):
        """Get Twitter API credentials from environment."""
        return {
            'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
            'api_key': os.getenv('TWITTER_API_KEY'),
            'api_secret': os.getenv('TWITTER_API_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        }
    
    @property
    def database_url(self):
        """Get database URL."""
        return os.getenv('DATABASE_URL', 'sqlite:///data/stock_sentiment.db')
