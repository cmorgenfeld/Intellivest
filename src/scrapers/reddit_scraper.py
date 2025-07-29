"""
Reddit scraper for r/WallStreetBets sentiment analysis.
"""

import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

try:
    import praw
except ImportError:
    praw = None

from ..utils.config import Config
from ..utils.helpers import extract_stock_symbols, clean_text

logger = logging.getLogger(__name__)


class RedditScraper:
    """Scraper for Reddit r/WallStreetBets posts."""
    
    def __init__(self):
        self.config = Config()
        self.reddit_config = self.config.reddit_config
        self.credentials = self.config.reddit_credentials
        self.reddit = self._initialize_reddit()
    
    def _initialize_reddit(self):
        """Initialize Reddit API connection."""
        if not praw:
            logger.error("praw library not installed. Install with: pip install praw")
            return None
            
        if not all(self.credentials.values()):
            logger.warning("Reddit credentials not found. Scraping will be limited.")
            return None
        
        try:
            reddit = praw.Reddit(
                client_id=self.credentials['client_id'],
                client_secret=self.credentials['client_secret'],
                user_agent=self.credentials['user_agent']
            )
            
            # Test connection
            reddit.user.me()
            logger.info("Reddit API connection established successfully")
            return reddit
            
        except Exception as e:
            logger.error(f"Failed to initialize Reddit API: {e}")
            return None
    
    async def scrape_wallstreetbets(self) -> List[Dict[str, Any]]:
        """
        Scrape posts from r/WallStreetBets.
        
        Returns:
            List of post data dictionaries
        """
        if not self.reddit:
            logger.error("Reddit API not initialized")
            return []
        
        posts_data = []
        subreddit_name = self.reddit_config.get('subreddit', 'wallstreetbets')
        sort_by = self.reddit_config.get('sort_by', 'hot')
        limit = self.reddit_config.get('limit', 100)
        time_filter = self.reddit_config.get('time_filter', 'day')
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get posts based on sort method
            if sort_by == 'hot':
                posts = subreddit.hot(limit=limit)
            elif sort_by == 'new':
                posts = subreddit.new(limit=limit)
            elif sort_by == 'top':
                posts = subreddit.top(time_filter=time_filter, limit=limit)
            elif sort_by == 'rising':
                posts = subreddit.rising(limit=limit)
            else:
                posts = subreddit.hot(limit=limit)
            
            for post in posts:
                # Extract stock symbols from title and text
                title_symbols = extract_stock_symbols(post.title)
                text_symbols = extract_stock_symbols(post.selftext or '')
                all_symbols = list(set(title_symbols + text_symbols))
                
                if all_symbols:  # Only include posts mentioning stocks
                    post_data = {
                        'id': post.id,
                        'title': post.title,
                        'text': clean_text(post.selftext or ''),
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author) if post.author else '[deleted]',
                        'symbols': all_symbols,
                        'url': post.url,
                        'source': 'reddit'
                    }
                    posts_data.append(post_data)
            
            logger.info(f"Scraped {len(posts_data)} posts from r/{subreddit_name}")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
            return []
    
    async def scrape_recent_hot_posts(self, limit=100):
        """
        Scrape recent hot posts for additional current sentiment data.
        
        Args:
            limit: Number of hot posts to scrape
            
        Returns:
            List of post data dictionaries
        """
        if not self.reddit:
            logger.error("Reddit API not initialized")
            return []
        
        posts_data = []
        subreddit_name = self.reddit_config.get('subreddit', 'wallstreetbets')
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = subreddit.hot(limit=limit)
            
            for post in posts:
                # Extract stock symbols from title and text
                title_symbols = extract_stock_symbols(post.title)
                text_symbols = extract_stock_symbols(post.selftext or '')
                all_symbols = list(set(title_symbols + text_symbols))
                
                if all_symbols:  # Only include posts mentioning stocks
                    post_data = {
                        'id': f"hot_{post.id}",  # Prefix to avoid duplicates
                        'title': post.title,
                        'text': clean_text(post.selftext or ''),
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author) if post.author else '[deleted]',
                        'symbols': all_symbols,
                        'url': post.url,
                        'source': 'reddit_hot'
                    }
                    posts_data.append(post_data)
            
            logger.info(f"Scraped {len(posts_data)} additional hot posts from r/{subreddit_name}")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error scraping hot posts: {e}")
            return []
    
    async def get_post_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get comments for a specific post.
        
        Args:
            post_id: Reddit post ID
            limit: Maximum number of comments to fetch
            
        Returns:
            List of comment data dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  # Remove "load more comments"
            
            comments_data = []
            for comment in submission.comments.list()[:limit]:
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    symbols = extract_stock_symbols(comment.body)
                    if symbols:
                        comment_data = {
                            'id': comment.id,
                            'body': clean_text(comment.body),
                            'score': comment.score,
                            'created_utc': datetime.fromtimestamp(comment.created_utc),
                            'author': str(comment.author) if comment.author else '[deleted]',
                            'symbols': symbols,
                            'post_id': post_id,
                            'source': 'reddit_comment'
                        }
                        comments_data.append(comment_data)
            
            return comments_data
            
        except Exception as e:
            logger.error(f"Error fetching comments for post {post_id}: {e}")
            return []
