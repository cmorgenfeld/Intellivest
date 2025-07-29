"""
Tests for the analysis modules.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime

from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.stock_ranker import StockRanker


class TestSentimentAnalyzer:
    """Test cases for sentiment analyzer."""
    
    def test_initialization(self):
        """Test sentiment analyzer initialization."""
        analyzer = SentimentAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'config')
        assert hasattr(analyzer, 'sentiment_config')
    
    def test_analyze_text_basic(self):
        """Test basic text sentiment analysis."""
        analyzer = SentimentAnalyzer()
        
        # Test positive text
        positive_text = "This stock is going to the moon! Great buy!"
        result = analyzer.analyze_text(positive_text)
        
        assert isinstance(result, dict)
        assert 'positive' in result
        assert 'negative' in result
        assert 'neutral' in result
        assert 'compound' in result
        assert result['compound'] > 0  # Should be positive
    
    def test_analyze_text_negative(self):
        """Test negative sentiment analysis."""
        analyzer = SentimentAnalyzer()
        
        negative_text = "This stock is crashing! Sell everything!"
        result = analyzer.analyze_text(negative_text)
        
        assert result['compound'] < 0  # Should be negative
    
    def test_analyze_posts_structure(self):
        """Test posts analysis structure."""
        analyzer = SentimentAnalyzer()
        
        mock_posts = [
            {
                'title': 'AAPL to the moon!',
                'text': 'Great earnings report',
                'symbols': ['AAPL'],
                'score': 100,
                'upvote_ratio': 0.9,
                'num_comments': 50
            }
        ]
        
        result = analyzer.analyze_posts(mock_posts)
        
        assert 'posts' in result
        assert 'symbol_sentiment' in result
        assert 'total_posts' in result
        assert 'symbols_mentioned' in result
        assert len(result['posts']) == 1
        assert 'AAPL' in result['symbol_sentiment']


class TestStockRanker:
    """Test cases for stock ranker."""
    
    def test_initialization(self):
        """Test stock ranker initialization."""
        ranker = StockRanker()
        assert ranker is not None
        assert hasattr(ranker, 'config')
        assert hasattr(ranker, 'analysis_config')
    
    def test_calculate_stock_metrics(self):
        """Test stock metrics calculation."""
        ranker = StockRanker()
        
        reddit_data = {
            'compound': 0.5,
            'mentions': 10,
            'total_weight': 100,
            'positive': 0.7,
            'negative': 0.2
        }
        
        twitter_data = {
            'compound': 0.3,
            'mentions': 15,
            'total_weight': 200,
            'positive': 0.6,
            'negative': 0.3
        }
        
        metrics = ranker._calculate_stock_metrics('AAPL', reddit_data, twitter_data)
        
        assert metrics['symbol'] == 'AAPL'
        assert 'composite_score' in metrics
        assert 'composite_sentiment' in metrics
        assert 'momentum_score' in metrics
        assert 'confidence_score' in metrics
        assert metrics['total_mentions'] == 25
    
    def test_rank_stocks_basic(self):
        """Test basic stock ranking."""
        ranker = StockRanker()
        
        reddit_sentiment = {
            'symbol_sentiment': {
                'AAPL': {
                    'compound': 0.5,
                    'mentions': 10,
                    'total_weight': 100,
                    'positive': 0.7,
                    'negative': 0.2
                }
            }
        }
        
        twitter_sentiment = {
            'symbol_sentiment': {
                'AAPL': {
                    'compound': 0.3,
                    'mentions': 8,
                    'total_weight': 80,
                    'positive': 0.6,
                    'negative': 0.3
                }
            }
        }
        
        # Lower minimum mentions for test
        ranker.min_mentions = 5
        rankings = ranker.rank_stocks(reddit_sentiment, twitter_sentiment)
        
        assert len(rankings) == 1
        assert rankings[0]['symbol'] == 'AAPL'
        assert rankings[0]['rank'] == 1


if __name__ == "__main__":
    pytest.main([__file__])
