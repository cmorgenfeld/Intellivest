"""
Sentiment analysis for stock-related social media posts.
"""

import logging
from typing import List, Dict, Any, Union
from collections import defaultdict

try:
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import nltk
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        
    try:
        nltk.data.find('corpora/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')
        
except ImportError as e:
    logging.warning(f"Some sentiment analysis libraries not available: {e}")
    TextBlob = None
    SentimentIntensityAnalyzer = None

from ..utils.config import Config
from ..utils.helpers import extract_stock_symbols

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment analysis engine for social media posts."""
    
    def __init__(self):
        self.config = Config()
        self.sentiment_config = self.config.sentiment_config
        self.model_type = self.sentiment_config.get('model', 'vader')
        self.threshold = self.sentiment_config.get('threshold', 0.1)
        
        # Initialize sentiment analyzers
        self.vader_analyzer = self._initialize_vader()
        
    def _initialize_vader(self):
        """Initialize VADER sentiment analyzer."""
        if SentimentIntensityAnalyzer:
            return SentimentIntensityAnalyzer()
        else:
            logger.warning("VADER sentiment analyzer not available")
            return None
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        if self.model_type == 'vader' and self.vader_analyzer:
            return self._analyze_with_vader(text)
        elif self.model_type == 'textblob' and TextBlob:
            return self._analyze_with_textblob(text)
        else:
            # Fallback to simple keyword-based analysis
            return self._analyze_with_keywords(text)
    
    def _analyze_with_vader(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using VADER."""
        scores = self.vader_analyzer.polarity_scores(text)
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }
    
    def _analyze_with_textblob(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using TextBlob."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Convert to similar format as VADER
        if polarity > 0:
            positive = polarity
            negative = 0
        else:
            positive = 0
            negative = abs(polarity)
        
        neutral = 1 - positive - negative
        
        return {
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'compound': polarity
        }
    
    def _analyze_with_keywords(self, text: str) -> Dict[str, float]:
        """Simple keyword-based sentiment analysis."""
        positive_keywords = [
            'buy', 'bull', 'bullish', 'moon', 'rocket', 'gain', 'profit', 'long',
            'call', 'calls', 'up', 'rise', 'pump', 'diamond hands', 'hodl', 'hold'
        ]
        
        negative_keywords = [
            'sell', 'bear', 'bearish', 'crash', 'loss', 'short', 'put', 'puts',
            'down', 'fall', 'dump', 'paper hands', 'rip', 'dead'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0, 'compound': 0.0}
        
        positive_score = positive_count / total
        negative_score = negative_count / total
        compound = (positive_count - negative_count) / total
        
        return {
            'positive': positive_score,
            'negative': negative_score,
            'neutral': max(0, 1 - positive_score - negative_score),
            'compound': compound
        }
    
    def analyze_posts(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment for Reddit posts.
        
        Args:
            posts: List of Reddit post dictionaries
            
        Returns:
            Dictionary with aggregated sentiment by stock symbol
        """
        symbol_sentiments = defaultdict(list)
        analyzed_posts = []
        
        for post in posts:
            # Combine title and text for analysis
            full_text = f"{post.get('title', '')} {post.get('text', '')}"
            sentiment = self.analyze_text(full_text)
            
            # Add sentiment to post data
            post_with_sentiment = post.copy()
            post_with_sentiment['sentiment'] = sentiment
            analyzed_posts.append(post_with_sentiment)
            
            # Aggregate by stock symbols
            for symbol in post.get('symbols', []):
                symbol_sentiments[symbol].append({
                    'sentiment': sentiment,
                    'score': post.get('score', 0),
                    'upvote_ratio': post.get('upvote_ratio', 0.5),
                    'num_comments': post.get('num_comments', 0)
                })
        
        # Calculate aggregated sentiment scores
        aggregated_sentiment = self._aggregate_sentiment_by_symbol(symbol_sentiments)
        
        return {
            'posts': analyzed_posts,
            'symbol_sentiment': aggregated_sentiment,
            'total_posts': len(posts),
            'symbols_mentioned': list(symbol_sentiments.keys())
        }
    
    def analyze_tweets(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment for tweets.
        
        Args:
            tweets: List of tweet dictionaries
            
        Returns:
            Dictionary with aggregated sentiment by stock symbol
        """
        symbol_sentiments = defaultdict(list)
        analyzed_tweets = []
        
        for tweet in tweets:
            sentiment = self.analyze_text(tweet.get('text', ''))
            
            # Add sentiment to tweet data
            tweet_with_sentiment = tweet.copy()
            tweet_with_sentiment['sentiment'] = sentiment
            analyzed_tweets.append(tweet_with_sentiment)
            
            # Aggregate by stock symbols
            for symbol in tweet.get('symbols', []):
                symbol_sentiments[symbol].append({
                    'sentiment': sentiment,
                    'like_count': tweet.get('like_count', 0),
                    'retweet_count': tweet.get('retweet_count', 0),
                    'reply_count': tweet.get('reply_count', 0)
                })
        
        # Calculate aggregated sentiment scores
        aggregated_sentiment = self._aggregate_sentiment_by_symbol(symbol_sentiments)
        
        return {
            'tweets': analyzed_tweets,
            'symbol_sentiment': aggregated_sentiment,
            'total_tweets': len(tweets),
            'symbols_mentioned': list(symbol_sentiments.keys())
        }
    
    def _aggregate_sentiment_by_symbol(self, symbol_sentiments: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """Aggregate sentiment scores by stock symbol."""
        aggregated = {}
        
        for symbol, sentiments in symbol_sentiments.items():
            if not sentiments:
                continue
            
            # Calculate weighted averages
            total_weight = 0
            weighted_positive = 0
            weighted_negative = 0
            weighted_compound = 0
            
            for item in sentiments:
                sentiment = item['sentiment']
                
                # Use engagement metrics as weights
                weight = 1
                if 'score' in item:  # Reddit post
                    weight = max(1, item['score'] * item.get('upvote_ratio', 0.5))
                elif 'like_count' in item:  # Tweet
                    weight = max(1, item['like_count'] + item['retweet_count'])
                
                weighted_positive += sentiment['positive'] * weight
                weighted_negative += sentiment['negative'] * weight
                weighted_compound += sentiment['compound'] * weight
                total_weight += weight
            
            if total_weight > 0:
                aggregated[symbol] = {
                    'positive': weighted_positive / total_weight,
                    'negative': weighted_negative / total_weight,
                    'compound': weighted_compound / total_weight,
                    'mentions': len(sentiments),
                    'total_weight': total_weight
                }
        
        return aggregated
