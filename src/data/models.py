"""
Data models for the stock sentiment analysis project.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class SentimentScore:
    """Sentiment analysis results."""
    positive: float
    negative: float
    neutral: float
    compound: float


@dataclass
class RedditPost:
    """Reddit post data model."""
    id: str
    title: str
    text: str
    score: int
    upvote_ratio: float
    num_comments: int
    created_utc: datetime
    author: str
    symbols: List[str]
    url: str
    sentiment: Optional[SentimentScore] = None
    source: str = 'reddit'


@dataclass
class Tweet:
    """Twitter tweet data model."""
    id: str
    text: str
    created_at: datetime
    author_id: str
    symbols: List[str]
    retweet_count: int = 0
    like_count: int = 0
    reply_count: int = 0
    quote_count: int = 0
    sentiment: Optional[SentimentScore] = None
    source: str = 'twitter'


@dataclass
class SymbolSentiment:
    """Aggregated sentiment data for a stock symbol."""
    symbol: str
    positive: float
    negative: float
    compound: float
    mentions: int
    total_weight: float
    source: str


@dataclass
class StockRanking:
    """Stock ranking with comprehensive metrics."""
    symbol: str
    rank: int
    composite_score: float
    composite_sentiment: float
    momentum_score: float
    confidence_score: float
    total_mentions: int
    reddit_mentions: int
    twitter_mentions: int
    reddit_sentiment: float
    twitter_sentiment: float
    reddit_positive: float
    reddit_negative: float
    twitter_positive: float
    twitter_negative: float
    reddit_engagement: float
    twitter_engagement: float
    timestamp: datetime


@dataclass
class AnalysisResult:
    """Complete analysis result containing all data."""
    reddit_data: Dict[str, Any]
    twitter_data: Dict[str, Any]
    stock_rankings: List[StockRanking]
    analysis_timestamp: datetime
    total_posts_analyzed: int
    total_tweets_analyzed: int
    symbols_analyzed: List[str]


@dataclass
class ApiCredentials:
    """API credentials container."""
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_token_secret: Optional[str] = None


@dataclass
class AnalysisConfig:
    """Configuration for analysis parameters."""
    reddit_subreddit: str = 'wallstreetbets'
    reddit_sort_by: str = 'hot'
    reddit_limit: int = 100
    reddit_time_filter: str = 'day'
    twitter_search_terms: List[str] = None
    twitter_max_tweets: int = 500
    twitter_include_retweets: bool = False
    sentiment_model: str = 'vader'
    sentiment_threshold: float = 0.1
    min_mentions: int = 5
    reddit_weight: float = 0.6
    twitter_weight: float = 0.4
    analysis_window_hours: int = 24
    
    def __post_init__(self):
        if self.twitter_search_terms is None:
            self.twitter_search_terms = ['$SPY', '$AAPL', '$TSLA', '$NVDA']


def convert_dict_to_sentiment_score(data: Dict[str, float]) -> SentimentScore:
    """Convert dictionary to SentimentScore object."""
    return SentimentScore(
        positive=data.get('positive', 0.0),
        negative=data.get('negative', 0.0),
        neutral=data.get('neutral', 0.0),
        compound=data.get('compound', 0.0)
    )


def convert_dict_to_reddit_post(data: Dict[str, Any]) -> RedditPost:
    """Convert dictionary to RedditPost object."""
    sentiment = None
    if 'sentiment' in data:
        sentiment = convert_dict_to_sentiment_score(data['sentiment'])
    
    return RedditPost(
        id=data.get('id', ''),
        title=data.get('title', ''),
        text=data.get('text', ''),
        score=data.get('score', 0),
        upvote_ratio=data.get('upvote_ratio', 0.5),
        num_comments=data.get('num_comments', 0),
        created_utc=data.get('created_utc', datetime.now()),
        author=data.get('author', ''),
        symbols=data.get('symbols', []),
        url=data.get('url', ''),
        sentiment=sentiment,
        source=data.get('source', 'reddit')
    )


def convert_dict_to_tweet(data: Dict[str, Any]) -> Tweet:
    """Convert dictionary to Tweet object."""
    sentiment = None
    if 'sentiment' in data:
        sentiment = convert_dict_to_sentiment_score(data['sentiment'])
    
    return Tweet(
        id=data.get('id', ''),
        text=data.get('text', ''),
        created_at=data.get('created_at', datetime.now()),
        author_id=data.get('author_id', ''),
        symbols=data.get('symbols', []),
        retweet_count=data.get('retweet_count', 0),
        like_count=data.get('like_count', 0),
        reply_count=data.get('reply_count', 0),
        quote_count=data.get('quote_count', 0),
        sentiment=sentiment,
        source=data.get('source', 'twitter')
    )


def convert_dict_to_stock_ranking(data: Dict[str, Any]) -> StockRanking:
    """Convert dictionary to StockRanking object."""
    return StockRanking(
        symbol=data.get('symbol', ''),
        rank=data.get('rank', 0),
        composite_score=data.get('composite_score', 0.0),
        composite_sentiment=data.get('composite_sentiment', 0.0),
        momentum_score=data.get('momentum_score', 0.0),
        confidence_score=data.get('confidence_score', 0.0),
        total_mentions=data.get('total_mentions', 0),
        reddit_mentions=data.get('reddit_mentions', 0),
        twitter_mentions=data.get('twitter_mentions', 0),
        reddit_sentiment=data.get('reddit_sentiment', 0.0),
        twitter_sentiment=data.get('twitter_sentiment', 0.0),
        reddit_positive=data.get('reddit_positive', 0.0),
        reddit_negative=data.get('reddit_negative', 0.0),
        twitter_positive=data.get('twitter_positive', 0.0),
        twitter_negative=data.get('twitter_negative', 0.0),
        reddit_engagement=data.get('reddit_engagement', 0.0),
        twitter_engagement=data.get('twitter_engagement', 0.0),
        timestamp=data.get('timestamp', datetime.now())
    )
