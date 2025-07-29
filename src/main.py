"""
Main application entry point for the Stock Sentiment Analysis project.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path

from src.utils.config import Config
from src.scrapers.reddit_scraper import RedditScraper
from src.scrapers.twitter_scraper import TwitterScraper
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.stock_ranker import StockRanker
from src.data.database import Database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockSentimentAnalyzer:
    """Main application class for stock sentiment analysis."""
    
    def __init__(self):
        self.config = Config()
        self.db = Database()
        self.reddit_scraper = RedditScraper()
        self.twitter_scraper = TwitterScraper()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.stock_ranker = StockRanker()
    
    def _configure_extended_collection(self):
        """Configure for extended data collection."""
        # Temporarily override config for more comprehensive collection
        self.reddit_scraper.reddit_config.update({
            'limit': 300,
            'sort_by': 'top',
            'time_filter': 'week'
        })
        logger.info("Configured for extended collection: 300 posts from past week")
    
    def _configure_comprehensive_collection(self):
        """Configure for comprehensive data collection."""
        self.reddit_scraper.reddit_config.update({
            'limit': 500,
            'sort_by': 'top', 
            'time_filter': 'month'
        })
        logger.info("Configured for comprehensive collection: 500 posts from past month")
    
    async def run_analysis(self, collection_mode="normal"):
        """
        Run the complete sentiment analysis pipeline.
        
        Args:
            collection_mode: "normal", "extended", or "comprehensive"
        """
        logger.info(f"Starting stock sentiment analysis in {collection_mode} mode...")
        
        # Adjust collection parameters based on mode
        if collection_mode == "extended":
            self._configure_extended_collection()
        elif collection_mode == "comprehensive":
            self._configure_comprehensive_collection()
        
        try:
            # Scrape data from Reddit
            logger.info("Scraping Reddit data...")
            reddit_data = await self.reddit_scraper.scrape_wallstreetbets()
            
            # If we're in extended mode, also get recent hot posts
            if collection_mode in ["extended", "comprehensive"]:
                logger.info("Scraping additional recent hot posts...")
                hot_data = await self.reddit_scraper.scrape_recent_hot_posts()
                reddit_data.extend(hot_data)
            
            # Scrape data from Twitter
            logger.info("Scraping Twitter data...")
            twitter_data = await self.twitter_scraper.scrape_stock_tweets()
            
            # Analyze sentiment
            logger.info("Analyzing sentiment...")
            reddit_sentiment = self.sentiment_analyzer.analyze_posts(reddit_data)
            twitter_sentiment = self.sentiment_analyzer.analyze_tweets(twitter_data)
            
            # Store data in database
            logger.info("Storing data in database...")
            self.db.store_reddit_data(reddit_sentiment)
            self.db.store_twitter_data(twitter_sentiment)
            
            # Rank stocks
            logger.info("Ranking stocks...")
            stock_rankings = self.stock_ranker.rank_stocks(
                reddit_sentiment, twitter_sentiment
            )
            
            # Store rankings
            self.db.store_rankings(stock_rankings)
            
            logger.info("Analysis complete!")
            return stock_rankings
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
    
    def get_latest_rankings(self):
        """Get the most recent stock rankings."""
        return self.db.get_latest_rankings()


if __name__ == "__main__":
    analyzer = StockSentimentAnalyzer()
    asyncio.run(analyzer.run_analysis())
