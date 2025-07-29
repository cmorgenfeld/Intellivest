"""
Tests for the scraper modules.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.scrapers.reddit_scraper import RedditScraper
from src.scrapers.twitter_scraper import TwitterScraper


class TestRedditScraper:
    """Test cases for Reddit scraper."""
    
    def test_initialization(self):
        """Test Reddit scraper initialization."""
        scraper = RedditScraper()
        assert scraper is not None
        assert hasattr(scraper, 'config')
        assert hasattr(scraper, 'reddit_config')
    
    @patch('src.scrapers.reddit_scraper.praw')
    def test_initialize_reddit_success(self, mock_praw):
        """Test successful Reddit API initialization."""
        mock_reddit = Mock()
        mock_reddit.user.me.return_value = Mock()
        mock_praw.Reddit.return_value = mock_reddit
        
        scraper = RedditScraper()
        # Test would pass if credentials are available
        
    def test_extract_symbols_from_title(self):
        """Test symbol extraction from post titles."""
        from src.utils.helpers import extract_stock_symbols
        
        title = "YOLO into $AAPL and $TSLA calls!"
        symbols = extract_stock_symbols(title)
        assert 'AAPL' in symbols
        assert 'TSLA' in symbols


class TestTwitterScraper:
    """Test cases for Twitter scraper."""
    
    def test_initialization(self):
        """Test Twitter scraper initialization."""
        scraper = TwitterScraper()
        assert scraper is not None
        assert hasattr(scraper, 'config')
        assert hasattr(scraper, 'twitter_config')
    
    @patch('src.scrapers.twitter_scraper.tweepy')
    def test_initialize_twitter_success(self, mock_tweepy):
        """Test successful Twitter API initialization."""
        mock_client = Mock()
        mock_client.get_me.return_value = Mock()
        mock_tweepy.Client.return_value = mock_client
        
        scraper = TwitterScraper()
        # Test would pass if credentials are available
    
    def test_extract_symbols_from_tweet(self):
        """Test symbol extraction from tweets."""
        from src.utils.helpers import extract_stock_symbols
        
        tweet_text = "Just bought $SPY calls and $QQQ puts! 🚀"
        symbols = extract_stock_symbols(tweet_text)
        assert 'SPY' in symbols
        assert 'QQQ' in symbols


if __name__ == "__main__":
    pytest.main([__file__])
