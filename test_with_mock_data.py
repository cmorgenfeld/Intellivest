"""
Test script to run sentiment analysis with mock data (no API keys needed).
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.stock_ranker import StockRanker
from src.data.database import Database
from src.utils.helpers import setup_directories

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_mock_reddit_data():
    """Create mock Reddit data for testing."""
    return [
        {
            'id': 'post1',
            'title': 'YOLO into $AAPL calls! 🚀🚀🚀',
            'text': 'Apple is going to the moon! Diamond hands! This is the way!',
            'score': 1500,
            'upvote_ratio': 0.85,
            'num_comments': 200,
            'created_utc': datetime.now(),
            'author': 'test_user1',
            'symbols': ['AAPL'],
            'url': 'https://reddit.com/test1',
            'source': 'reddit'
        },
        {
            'id': 'post2', 
            'title': '$TSLA puts printing! 📉',
            'text': 'Tesla is overvalued, time to short. Paper hands selling.',
            'score': 800,
            'upvote_ratio': 0.65,
            'num_comments': 150,
            'created_utc': datetime.now(),
            'author': 'test_user2',
            'symbols': ['TSLA'],
            'url': 'https://reddit.com/test2',
            'source': 'reddit'
        },
        {
            'id': 'post3',
            'title': '$SPY and $QQQ looking bullish',
            'text': 'Market is strong, buying calls on both. Bull market continues!',
            'score': 2200,
            'upvote_ratio': 0.92,
            'num_comments': 300,
            'created_utc': datetime.now(),
            'author': 'test_user3',
            'symbols': ['SPY', 'QQQ'],
            'url': 'https://reddit.com/test3',
            'source': 'reddit'
        }
    ]


def create_mock_twitter_data():
    """Create mock Twitter data for testing."""
    return [
        {
            'id': 'tweet1',
            'text': 'Just bought more $AAPL shares! This company is unstoppable 🚀',
            'created_at': datetime.now(),
            'author_id': 'twitter_user1',
            'symbols': ['AAPL'],
            'like_count': 150,
            'retweet_count': 25,
            'reply_count': 10,
            'quote_count': 5,
            'source': 'twitter'
        },
        {
            'id': 'tweet2',
            'text': '$TSLA is crashing hard today. Glad I sold my calls yesterday.',
            'created_at': datetime.now(),
            'author_id': 'twitter_user2', 
            'symbols': ['TSLA'],
            'like_count': 89,
            'retweet_count': 12,
            'reply_count': 8,
            'quote_count': 2,
            'source': 'twitter'
        },
        {
            'id': 'tweet3',
            'text': '$SPY breaking resistance! New all-time highs incoming 📈',
            'created_at': datetime.now(),
            'author_id': 'twitter_user3',
            'symbols': ['SPY'],
            'like_count': 200,
            'retweet_count': 45,
            'reply_count': 15,
            'quote_count': 8,
            'source': 'twitter'
        }
    ]


async def test_sentiment_analysis():
    """Test the sentiment analysis pipeline with mock data."""
    logger.info("🧪 Starting sentiment analysis test with mock data...")
    
    try:
        # Setup directories
        setup_directories()
        
        # Create mock data
        mock_reddit_data = create_mock_reddit_data()
        mock_twitter_data = create_mock_twitter_data()
        
        logger.info(f"📊 Created {len(mock_reddit_data)} mock Reddit posts")
        logger.info(f"🐦 Created {len(mock_twitter_data)} mock tweets")
        
        # Initialize components
        sentiment_analyzer = SentimentAnalyzer()
        stock_ranker = StockRanker()
        db = Database()
        
        # Analyze sentiment
        logger.info("🔍 Analyzing Reddit sentiment...")
        reddit_sentiment = sentiment_analyzer.analyze_posts(mock_reddit_data)
        
        logger.info("🔍 Analyzing Twitter sentiment...")
        twitter_sentiment = sentiment_analyzer.analyze_tweets(mock_twitter_data)
        
        # Store data in database
        logger.info("💾 Storing data in database...")
        db.store_reddit_data(reddit_sentiment)
        db.store_twitter_data(twitter_sentiment)
        
        # Rank stocks
        logger.info("📈 Ranking stocks...")
        stock_rankings = stock_ranker.rank_stocks(reddit_sentiment, twitter_sentiment)
        
        # Store rankings
        db.store_rankings(stock_rankings)
        
        # Display results
        print("\n" + "="*70)
        print("🏆 MOCK DATA SENTIMENT ANALYSIS RESULTS")
        print("="*70)
        
        print(f"\n📊 Reddit Analysis:")
        print(f"   • Total posts analyzed: {reddit_sentiment['total_posts']}")
        print(f"   • Symbols mentioned: {', '.join(reddit_sentiment['symbols_mentioned'])}")
        
        print(f"\n🐦 Twitter Analysis:")
        print(f"   • Total tweets analyzed: {twitter_sentiment['total_tweets']}")
        print(f"   • Symbols mentioned: {', '.join(twitter_sentiment['symbols_mentioned'])}")
        
        print(f"\n🏆 TOP STOCK RANKINGS:")
        print("-" * 70)
        print(f"{'Rank':<4} {'Symbol':<8} {'Score':<8} {'Sentiment':<10} {'Mentions':<8} {'Confidence':<10}")
        print("-" * 70)
        
        for stock in stock_rankings[:10]:
            print(f"{stock['rank']:<4} {stock['symbol']:<8} "
                  f"{stock['composite_score']:<8.3f} {stock['composite_sentiment']:<10.3f} "
                  f"{stock['total_mentions']:<8} {stock['confidence_score']:<10.3f}")
        
        print("\n" + "="*70)
        print("✅ Test completed successfully!")
        print("🔧 Your sentiment analysis system is working correctly.")
        print("🔑 Now you just need to add your API keys to start scraping real data.")
        print("="*70)
        
        return stock_rankings
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_sentiment_analysis())
