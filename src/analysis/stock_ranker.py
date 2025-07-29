"""
Stock ranking system based on sentiment analysis.
"""

import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
from collections import defaultdict

from ..utils.config import Config

logger = logging.getLogger(__name__)


class StockRanker:
    """Stock ranking system based on sentiment analysis from multiple sources."""
    
    def __init__(self):
        self.config = Config()
        self.analysis_config = self.config.analysis_config
        self.min_mentions = self.analysis_config.get('min_mentions', 5)
        self.reddit_weight = self.analysis_config.get('weight_reddit', 0.6)
        self.twitter_weight = self.analysis_config.get('weight_twitter', 0.4)
    
    def rank_stocks(self, reddit_sentiment: Dict[str, Any], twitter_sentiment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank stocks based on combined sentiment from Reddit and Twitter.
        
        Args:
            reddit_sentiment: Sentiment analysis results from Reddit
            twitter_sentiment: Sentiment analysis results from Twitter
            
        Returns:
            List of ranked stocks with scores and metrics
        """
        # Get symbol sentiment data
        reddit_symbols = reddit_sentiment.get('symbol_sentiment', {})
        twitter_symbols = twitter_sentiment.get('symbol_sentiment', {})
        
        # Combine symbols from both sources
        all_symbols = set(list(reddit_symbols.keys()) + list(twitter_symbols.keys()))
        
        ranked_stocks = []
        
        for symbol in all_symbols:
            reddit_data = reddit_symbols.get(symbol, {})
            twitter_data = twitter_symbols.get(symbol, {})
            
            # Calculate combined metrics
            stock_metrics = self._calculate_stock_metrics(symbol, reddit_data, twitter_data)
            
            # Only include stocks with minimum mentions
            total_mentions = stock_metrics['reddit_mentions'] + stock_metrics['twitter_mentions']
            if total_mentions >= self.min_mentions:
                ranked_stocks.append(stock_metrics)
        
        # Sort by composite score (descending)
        ranked_stocks.sort(key=lambda x: x['composite_score'], reverse=True)
        
        # Add rankings
        for i, stock in enumerate(ranked_stocks):
            stock['rank'] = i + 1
        
        logger.info(f"Ranked {len(ranked_stocks)} stocks")
        return ranked_stocks
    
    def _calculate_stock_metrics(self, symbol: str, reddit_data: Dict, twitter_data: Dict) -> Dict[str, Any]:
        """
        Calculate comprehensive metrics for a stock symbol.
        
        Args:
            symbol: Stock symbol
            reddit_data: Reddit sentiment data for the symbol
            twitter_data: Twitter sentiment data for the symbol
            
        Returns:
            Dictionary with stock metrics and scores
        """
        # Extract Reddit metrics
        reddit_sentiment = reddit_data.get('compound', 0.0)
        reddit_mentions = reddit_data.get('mentions', 0)
        reddit_weight_total = reddit_data.get('total_weight', 0)
        reddit_positive = reddit_data.get('positive', 0.0)
        reddit_negative = reddit_data.get('negative', 0.0)
        
        # Extract Twitter metrics
        twitter_sentiment = twitter_data.get('compound', 0.0)
        twitter_mentions = twitter_data.get('mentions', 0)
        twitter_weight_total = twitter_data.get('total_weight', 0)
        twitter_positive = twitter_data.get('positive', 0.0)
        twitter_negative = twitter_data.get('negative', 0.0)
        
        # Calculate weighted composite sentiment
        total_weight = (reddit_weight_total * self.reddit_weight + 
                       twitter_weight_total * self.twitter_weight)
        
        if total_weight > 0:
            composite_sentiment = (
                reddit_sentiment * reddit_weight_total * self.reddit_weight +
                twitter_sentiment * twitter_weight_total * self.twitter_weight
            ) / total_weight
        else:
            composite_sentiment = 0.0
        
        # Calculate momentum score (based on mention volume and engagement)
        momentum_score = self._calculate_momentum_score(
            reddit_mentions, twitter_mentions, reddit_weight_total, twitter_weight_total
        )
        
        # Calculate composite score (combines sentiment and momentum)
        composite_score = (composite_sentiment * 0.7) + (momentum_score * 0.3)
        
        # Calculate confidence score based on data availability
        confidence_score = self._calculate_confidence_score(
            reddit_mentions, twitter_mentions, reddit_weight_total, twitter_weight_total
        )
        
        return {
            'symbol': symbol,
            'composite_score': round(composite_score, 4),
            'composite_sentiment': round(composite_sentiment, 4),
            'momentum_score': round(momentum_score, 4),
            'confidence_score': round(confidence_score, 4),
            'total_mentions': reddit_mentions + twitter_mentions,
            'reddit_mentions': reddit_mentions,
            'twitter_mentions': twitter_mentions,
            'reddit_sentiment': round(reddit_sentiment, 4),
            'twitter_sentiment': round(twitter_sentiment, 4),
            'reddit_positive': round(reddit_positive, 4),
            'reddit_negative': round(reddit_negative, 4),
            'twitter_positive': round(twitter_positive, 4),
            'twitter_negative': round(twitter_negative, 4),
            'reddit_engagement': reddit_weight_total,
            'twitter_engagement': twitter_weight_total,
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_momentum_score(self, reddit_mentions: int, twitter_mentions: int,
                                reddit_weight: float, twitter_weight: float) -> float:
        """
        Calculate momentum score based on mention volume and engagement.
        
        Returns:
            Normalized momentum score between 0 and 1
        """
        # Normalize mention counts (logarithmic scaling to handle outliers)
        import math
        
        reddit_momentum = math.log(reddit_mentions + 1) * math.log(reddit_weight + 1)
        twitter_momentum = math.log(twitter_mentions + 1) * math.log(twitter_weight + 1)
        
        total_momentum = reddit_momentum * self.reddit_weight + twitter_momentum * self.twitter_weight
        
        # Normalize to 0-1 scale using sigmoid function
        normalized_momentum = 2 / (1 + math.exp(-total_momentum / 10)) - 1
        
        return max(0, min(1, normalized_momentum))
    
    def _calculate_confidence_score(self, reddit_mentions: int, twitter_mentions: int,
                                  reddit_weight: float, twitter_weight: float) -> float:
        """
        Calculate confidence score based on data quality and quantity.
        
        Returns:
            Confidence score between 0 and 1
        """
        # Minimum thresholds for high confidence
        min_reddit_mentions = 3
        min_twitter_mentions = 5
        min_total_mentions = 8
        
        total_mentions = reddit_mentions + twitter_mentions
        
        # Base confidence from mention count
        mention_confidence = min(1.0, total_mentions / min_total_mentions)
        
        # Source diversity bonus (having data from both sources increases confidence)
        source_diversity = 0.5
        if reddit_mentions >= min_reddit_mentions and twitter_mentions >= min_twitter_mentions:
            source_diversity = 1.0
        elif reddit_mentions > 0 and twitter_mentions > 0:
            source_diversity = 0.8
        
        # Engagement quality (higher engagement = higher confidence)
        total_weight = reddit_weight + twitter_weight
        engagement_quality = min(1.0, total_weight / 100)  # Normalize based on expected engagement
        
        # Combined confidence score
        confidence = (mention_confidence * 0.4 + source_diversity * 0.4 + engagement_quality * 0.2)
        
        return round(confidence, 4)
    
    def get_top_stocks(self, ranked_stocks: List[Dict[str, Any]], count: int = 10) -> List[Dict[str, Any]]:
        """
        Get top N stocks from ranked list.
        
        Args:
            ranked_stocks: List of ranked stocks
            count: Number of top stocks to return
            
        Returns:
            List of top stocks
        """
        return ranked_stocks[:count]
    
    def filter_by_sentiment(self, ranked_stocks: List[Dict[str, Any]], 
                          min_sentiment: float = 0.1) -> List[Dict[str, Any]]:
        """
        Filter stocks by minimum sentiment threshold.
        
        Args:
            ranked_stocks: List of ranked stocks
            min_sentiment: Minimum composite sentiment score
            
        Returns:
            Filtered list of stocks
        """
        return [stock for stock in ranked_stocks 
                if stock['composite_sentiment'] >= min_sentiment]
    
    def filter_by_confidence(self, ranked_stocks: List[Dict[str, Any]], 
                           min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """
        Filter stocks by minimum confidence threshold.
        
        Args:
            ranked_stocks: List of ranked stocks
            min_confidence: Minimum confidence score
            
        Returns:
            Filtered list of stocks
        """
        return [stock for stock in ranked_stocks 
                if stock['confidence_score'] >= min_confidence]
