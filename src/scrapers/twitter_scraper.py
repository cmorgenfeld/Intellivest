"""
Twitter scraper for stock sentiment analysis.
"""

import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

try:
    import tweepy
except ImportError:
    tweepy = None

from ..utils.config import Config
from ..utils.helpers import extract_stock_symbols, clean_text

logger = logging.getLogger(__name__)


class TwitterScraper:
    """Scraper for Twitter stock-related tweets."""
    
    def __init__(self):
        self.config = Config()
        self.twitter_config = self.config.twitter_config
        self.credentials = self.config.twitter_credentials
        self.api = self._initialize_twitter()
    
    def _initialize_twitter(self):
        """Initialize Twitter API connection."""
        if not tweepy:
            logger.error("tweepy library not installed. Install with: pip install tweepy")
            return None
            
        if not all(self.credentials.values()):
            logger.warning("Twitter credentials not found. Scraping will be limited.")
            return None
        
        try:
            # Initialize Twitter API v2
            client = tweepy.Client(
                bearer_token=self.credentials['bearer_token'],
                consumer_key=self.credentials['api_key'],
                consumer_secret=self.credentials['api_secret'],
                access_token=self.credentials['access_token'],
                access_token_secret=self.credentials['access_token_secret'],
                wait_on_rate_limit=True
            )
            
            # Test connection
            me = client.get_me()
            logger.info("Twitter API connection established successfully")
            return client
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            return None
    
    async def scrape_stock_tweets(self) -> List[Dict[str, Any]]:
        """
        Scrape stock-related tweets.
        
        Returns:
            List of tweet data dictionaries
        """
        if not self.api:
            logger.error("Twitter API not initialized")
            return []
        
        tweets_data = []
        search_terms = self.twitter_config.get('search_terms', ['$SPY', '$AAPL'])
        max_tweets = self.twitter_config.get('max_tweets', 500)
        include_retweets = self.twitter_config.get('include_retweets', False)
        
        # Calculate tweets per search term
        tweets_per_term = max_tweets // len(search_terms)
        
        try:
            for term in search_terms:
                query = term
                if not include_retweets:
                    query += " -is:retweet"
                
                # Search for recent tweets
                tweets = tweepy.Paginator(
                    self.api.search_recent_tweets,
                    query=query,
                    tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations'],
                    max_results=min(100, tweets_per_term),  # Twitter API limit
                    limit=tweets_per_term // 100 + 1
                ).flatten(limit=tweets_per_term)
                
                for tweet in tweets:
                    # Extract stock symbols from tweet text
                    symbols = extract_stock_symbols(tweet.text)
                    
                    if symbols:  # Only include tweets mentioning stocks
                        tweet_data = {
                            'id': tweet.id,
                            'text': clean_text(tweet.text),
                            'created_at': tweet.created_at,
                            'author_id': tweet.author_id,
                            'symbols': symbols,
                            'source': 'twitter'
                        }
                        
                        # Add public metrics if available
                        if hasattr(tweet, 'public_metrics'):
                            tweet_data.update({
                                'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                                'like_count': tweet.public_metrics.get('like_count', 0),
                                'reply_count': tweet.public_metrics.get('reply_count', 0),
                                'quote_count': tweet.public_metrics.get('quote_count', 0)
                            })
                        
                        tweets_data.append(tweet_data)
            
            logger.info(f"Scraped {len(tweets_data)} tweets")
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error scraping Twitter: {e}")
            return []
    
    async def search_tweets_by_hashtag(self, hashtag: str, count: int = 100) -> List[Dict[str, Any]]:
        """
        Search tweets by hashtag.
        
        Args:
            hashtag: Hashtag to search for (without #)
            count: Number of tweets to fetch
            
        Returns:
            List of tweet data dictionaries
        """
        if not self.api:
            return []
        
        try:
            query = f"#{hashtag} -is:retweet"
            tweets = tweepy.Paginator(
                self.api.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'author_id', 'public_metrics'],
                max_results=min(100, count),
                limit=count // 100 + 1
            ).flatten(limit=count)
            
            tweets_data = []
            for tweet in tweets:
                symbols = extract_stock_symbols(tweet.text)
                
                tweet_data = {
                    'id': tweet.id,
                    'text': clean_text(tweet.text),
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'symbols': symbols,
                    'hashtag': hashtag,
                    'source': 'twitter_hashtag'
                }
                
                if hasattr(tweet, 'public_metrics'):
                    tweet_data.update({
                        'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                        'like_count': tweet.public_metrics.get('like_count', 0),
                        'reply_count': tweet.public_metrics.get('reply_count', 0),
                        'quote_count': tweet.public_metrics.get('quote_count', 0)
                    })
                
                tweets_data.append(tweet_data)
            
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error searching tweets by hashtag #{hashtag}: {e}")
            return []
