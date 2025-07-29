"""
Database operations for storing and retrieving sentiment analysis data.
"""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

from ..utils.config import Config

logger = logging.getLogger(__name__)


class Database:
    """Database manager for stock sentiment analysis data."""
    
    def __init__(self):
        self.config = Config()
        self.db_path = self._get_db_path()
        self._initialize_database()
    
    def _get_db_path(self) -> str:
        """Get database file path."""
        db_url = self.config.database_url
        if db_url.startswith('sqlite:///'):
            db_path = db_url.replace('sqlite:///', '')
            # Create directory if it doesn't exist
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            return db_path
        else:
            # Default to local database
            Path('data').mkdir(exist_ok=True)
            return 'data/stock_sentiment.db'
    
    def _initialize_database(self):
        """Initialize database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Reddit posts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reddit_posts (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        text TEXT,
                        score INTEGER,
                        upvote_ratio REAL,
                        num_comments INTEGER,
                        created_utc TIMESTAMP,
                        author TEXT,
                        symbols TEXT,
                        url TEXT,
                        sentiment_positive REAL,
                        sentiment_negative REAL,
                        sentiment_neutral REAL,
                        sentiment_compound REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Twitter tweets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS twitter_tweets (
                        id TEXT PRIMARY KEY,
                        text TEXT,
                        created_at TIMESTAMP,
                        author_id TEXT,
                        symbols TEXT,
                        retweet_count INTEGER DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        reply_count INTEGER DEFAULT 0,
                        quote_count INTEGER DEFAULT 0,
                        sentiment_positive REAL,
                        sentiment_negative REAL,
                        sentiment_neutral REAL,
                        sentiment_compound REAL,
                        stored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Stock rankings table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stock_rankings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        symbol TEXT,
                        rank INTEGER,
                        composite_score REAL,
                        composite_sentiment REAL,
                        momentum_score REAL,
                        confidence_score REAL,
                        total_mentions INTEGER,
                        reddit_mentions INTEGER,
                        twitter_mentions INTEGER,
                        reddit_sentiment REAL,
                        twitter_sentiment REAL,
                        reddit_positive REAL,
                        reddit_negative REAL,
                        twitter_positive REAL,
                        twitter_negative REAL,
                        reddit_engagement REAL,
                        twitter_engagement REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Symbol sentiment history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS symbol_sentiment_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        symbol TEXT,
                        source TEXT,
                        sentiment_compound REAL,
                        mentions INTEGER,
                        engagement_weight REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_reddit_symbols ON reddit_posts (symbols)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_reddit_created ON reddit_posts (created_utc)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_twitter_symbols ON twitter_tweets (symbols)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_twitter_created ON twitter_tweets (created_at)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_rankings_symbol ON stock_rankings (symbol)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_rankings_created ON stock_rankings (created_at)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def store_reddit_data(self, reddit_sentiment: Dict[str, Any]):
        """Store Reddit sentiment analysis data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                posts = reddit_sentiment.get('posts', [])
                for post in posts:
                    sentiment = post.get('sentiment', {})
                    symbols_str = ','.join(post.get('symbols', []))
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO reddit_posts
                        (id, title, text, score, upvote_ratio, num_comments, created_utc,
                         author, symbols, url, sentiment_positive, sentiment_negative,
                         sentiment_neutral, sentiment_compound)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        post.get('id'),
                        post.get('title'),
                        post.get('text'),
                        post.get('score', 0),
                        post.get('upvote_ratio', 0.5),
                        post.get('num_comments', 0),
                        post.get('created_utc'),
                        post.get('author'),
                        symbols_str,
                        post.get('url'),
                        sentiment.get('positive', 0.0),
                        sentiment.get('negative', 0.0),
                        sentiment.get('neutral', 0.0),
                        sentiment.get('compound', 0.0)
                    ))
                
                # Store symbol sentiment history
                symbol_sentiment = reddit_sentiment.get('symbol_sentiment', {})
                for symbol, data in symbol_sentiment.items():
                    cursor.execute('''
                        INSERT INTO symbol_sentiment_history
                        (symbol, source, sentiment_compound, mentions, engagement_weight)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        symbol,
                        'reddit',
                        data.get('compound', 0.0),
                        data.get('mentions', 0),
                        data.get('total_weight', 0.0)
                    ))
                
                conn.commit()
                logger.info(f"Stored {len(posts)} Reddit posts")
                
        except Exception as e:
            logger.error(f"Error storing Reddit data: {e}")
    
    def store_twitter_data(self, twitter_sentiment: Dict[str, Any]):
        """Store Twitter sentiment analysis data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tweets = twitter_sentiment.get('tweets', [])
                for tweet in tweets:
                    sentiment = tweet.get('sentiment', {})
                    symbols_str = ','.join(tweet.get('symbols', []))
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO twitter_tweets
                        (id, text, created_at, author_id, symbols, retweet_count,
                         like_count, reply_count, quote_count, sentiment_positive,
                         sentiment_negative, sentiment_neutral, sentiment_compound)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        tweet.get('id'),
                        tweet.get('text'),
                        tweet.get('created_at'),
                        tweet.get('author_id'),
                        symbols_str,
                        tweet.get('retweet_count', 0),
                        tweet.get('like_count', 0),
                        tweet.get('reply_count', 0),
                        tweet.get('quote_count', 0),
                        sentiment.get('positive', 0.0),
                        sentiment.get('negative', 0.0),
                        sentiment.get('neutral', 0.0),
                        sentiment.get('compound', 0.0)
                    ))
                
                # Store symbol sentiment history
                symbol_sentiment = twitter_sentiment.get('symbol_sentiment', {})
                for symbol, data in symbol_sentiment.items():
                    cursor.execute('''
                        INSERT INTO symbol_sentiment_history
                        (symbol, source, sentiment_compound, mentions, engagement_weight)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        symbol,
                        'twitter',
                        data.get('compound', 0.0),
                        data.get('mentions', 0),
                        data.get('total_weight', 0.0)
                    ))
                
                conn.commit()
                logger.info(f"Stored {len(tweets)} tweets")
                
        except Exception as e:
            logger.error(f"Error storing Twitter data: {e}")
    
    def store_rankings(self, rankings: List[Dict[str, Any]]):
        """Store stock rankings."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for stock in rankings:
                    cursor.execute('''
                        INSERT INTO stock_rankings
                        (symbol, rank, composite_score, composite_sentiment, momentum_score,
                         confidence_score, total_mentions, reddit_mentions, twitter_mentions,
                         reddit_sentiment, twitter_sentiment, reddit_positive, reddit_negative,
                         twitter_positive, twitter_negative, reddit_engagement, twitter_engagement)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        stock.get('symbol'),
                        stock.get('rank'),
                        stock.get('composite_score'),
                        stock.get('composite_sentiment'),
                        stock.get('momentum_score'),
                        stock.get('confidence_score'),
                        stock.get('total_mentions'),
                        stock.get('reddit_mentions'),
                        stock.get('twitter_mentions'),
                        stock.get('reddit_sentiment'),
                        stock.get('twitter_sentiment'),
                        stock.get('reddit_positive'),
                        stock.get('reddit_negative'),
                        stock.get('twitter_positive'),
                        stock.get('twitter_negative'),
                        stock.get('reddit_engagement'),
                        stock.get('twitter_engagement')
                    ))
                
                conn.commit()
                logger.info(f"Stored rankings for {len(rankings)} stocks")
                
        except Exception as e:
            logger.error(f"Error storing rankings: {e}")
    
    def get_latest_rankings(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get the most recent stock rankings."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM stock_rankings
                    WHERE created_at = (
                        SELECT MAX(created_at) FROM stock_rankings
                    )
                    ORDER BY rank
                    LIMIT ?
                ''', (limit,))
                
                columns = [description[0] for description in cursor.description]
                rankings = []
                
                for row in cursor.fetchall():
                    ranking = dict(zip(columns, row))
                    rankings.append(ranking)
                
                return rankings
                
        except Exception as e:
            logger.error(f"Error getting latest rankings: {e}")
            return []
    
    def get_symbol_history(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get historical sentiment data for a symbol."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT * FROM symbol_sentiment_history
                    WHERE symbol = ? AND created_at >= ?
                    ORDER BY created_at DESC
                ''', (symbol, cutoff_date))
                
                columns = [description[0] for description in cursor.description]
                history = []
                
                for row in cursor.fetchall():
                    record = dict(zip(columns, row))
                    history.append(record)
                
                return history
                
        except Exception as e:
            logger.error(f"Error getting symbol history for {symbol}: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data beyond specified days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                # Clean up old posts and tweets
                cursor.execute('DELETE FROM reddit_posts WHERE created_utc < ?', (cutoff_date,))
                cursor.execute('DELETE FROM twitter_tweets WHERE created_at < ?', (cutoff_date,))
                cursor.execute('DELETE FROM symbol_sentiment_history WHERE created_at < ?', (cutoff_date,))
                
                # Keep only latest ranking per day for historical analysis
                cursor.execute('''
                    DELETE FROM stock_rankings 
                    WHERE created_at < ? 
                    AND id NOT IN (
                        SELECT MIN(id) 
                        FROM stock_rankings 
                        WHERE created_at < ?
                        GROUP BY DATE(created_at), symbol
                    )
                ''', (cutoff_date, cutoff_date))
                
                conn.commit()
                logger.info(f"Cleaned up data older than {days} days")
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Count records in each table
                tables = ['reddit_posts', 'twitter_tweets', 'stock_rankings', 'symbol_sentiment_history']
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[table] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
