"""
Historical backtesting module to analyze correlation between sentiment and stock price movements.
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import sqlite3

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logging.warning("yfinance not available. Install with: pip install yfinance")

from ..utils.config import Config

logger = logging.getLogger(__name__)


class SentimentBacktester:
    """Backtesting engine to validate sentiment analysis against historical price movements."""
    
    def __init__(self, db_path="data/stock_sentiment.db"):
        self.config = Config()
        self.db_path = db_path
        
    def get_historical_sentiment_data(self, days_back=30) -> pd.DataFrame:
        """
        Get historical sentiment rankings from database.
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            DataFrame with historical sentiment data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get historical rankings
            query = """
            SELECT 
                symbol,
                composite_score,
                composite_sentiment, 
                confidence_score,
                total_mentions,
                reddit_mentions,
                reddit_engagement,
                created_at,
                DATE(created_at) as date
            FROM stock_rankings 
            WHERE created_at >= datetime('now', '-{} days')
            ORDER BY created_at DESC, composite_score DESC
            """.format(days_back)
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['date'] = pd.to_datetime(df['date'])
                
            logger.info(f"Retrieved {len(df)} historical sentiment records")
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving historical sentiment data: {e}")
            return pd.DataFrame()
    
    def get_stock_price_data(self, symbols: List[str], days_back=30) -> Dict[str, pd.DataFrame]:
        """
        Get historical stock price data for given symbols.
        
        Args:
            symbols: List of stock symbols
            days_back: Number of days to look back
            
        Returns:
            Dictionary mapping symbols to price DataFrames
        """
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance not available for price data")
            return {}
        
        price_data = {}
        start_date = datetime.now() - timedelta(days=days_back + 5)  # Extra buffer
        end_date = datetime.now()
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                
                if not hist.empty:
                    # Calculate daily returns
                    hist['Daily_Return'] = hist['Close'].pct_change()
                    hist['Forward_1d_Return'] = hist['Daily_Return'].shift(-1)  # Next day return
                    hist['Forward_3d_Return'] = hist['Close'].pct_change(periods=-3)  # 3-day forward return
                    hist['Forward_7d_Return'] = hist['Close'].pct_change(periods=-7)  # 7-day forward return
                    
                    price_data[symbol] = hist
                    logger.info(f"Retrieved price data for {symbol}: {len(hist)} days")
                else:
                    logger.warning(f"No price data found for {symbol}")
                    
            except Exception as e:
                logger.error(f"Error getting price data for {symbol}: {e}")
        
        return price_data
    
    def calculate_sentiment_accuracy(self, sentiment_df: pd.DataFrame, price_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Calculate how well sentiment predicts price movements.
        
        Args:
            sentiment_df: Historical sentiment data
            price_data: Historical price data
            
        Returns:
            Dictionary with accuracy metrics
        """
        results = {
            'total_predictions': 0,
            'correct_predictions_1d': 0,
            'correct_predictions_3d': 0,
            'correct_predictions_7d': 0,
            'accuracy_1d': 0.0,
            'accuracy_3d': 0.0,
            'accuracy_7d': 0.0,
            'correlations': {},
            'detailed_results': []
        }
        
        for _, row in sentiment_df.iterrows():
            symbol = row['symbol']
            sentiment_date = row['date']
            sentiment_score = row['composite_sentiment']
            confidence = row['confidence_score']
            
            if symbol not in price_data:
                continue
                
            # Find price data for the sentiment date
            symbol_prices = price_data[symbol]
            
            # Match dates (allowing for weekends/holidays)
            date_matches = symbol_prices.index.date >= sentiment_date.date()
            if not date_matches.any():
                continue
                
            # Get the first trading day on or after sentiment date
            price_row_idx = symbol_prices.index[date_matches][0]
            price_row = symbol_prices.loc[price_row_idx]
            
            # Get forward returns
            forward_1d = price_row.get('Forward_1d_Return', np.nan)
            forward_3d = price_row.get('Forward_3d_Return', np.nan)
            forward_7d = price_row.get('Forward_7d_Return', np.nan)
            
            if pd.isna(forward_1d) and pd.isna(forward_3d) and pd.isna(forward_7d):
                continue
            
            results['total_predictions'] += 1
            
            # Predict direction based on sentiment
            predicted_direction = 1 if sentiment_score > 0 else -1
            
            # Check accuracy for different time horizons
            if not pd.isna(forward_1d):
                actual_direction_1d = 1 if forward_1d > 0 else -1
                if predicted_direction == actual_direction_1d:
                    results['correct_predictions_1d'] += 1
            
            if not pd.isna(forward_3d):
                actual_direction_3d = 1 if forward_3d > 0 else -1
                if predicted_direction == actual_direction_3d:
                    results['correct_predictions_3d'] += 1
            
            if not pd.isna(forward_7d):
                actual_direction_7d = 1 if forward_7d > 0 else -1
                if predicted_direction == actual_direction_7d:
                    results['correct_predictions_7d'] += 1
            
            # Store detailed result
            results['detailed_results'].append({
                'symbol': symbol,
                'date': sentiment_date,
                'sentiment_score': sentiment_score,
                'confidence_score': confidence,
                'forward_1d_return': forward_1d,
                'forward_3d_return': forward_3d,
                'forward_7d_return': forward_7d,
                'predicted_direction': predicted_direction
            })
        
        # Calculate accuracy rates
        if results['total_predictions'] > 0:
            results['accuracy_1d'] = results['correct_predictions_1d'] / results['total_predictions']
            results['accuracy_3d'] = results['correct_predictions_3d'] / results['total_predictions']
            results['accuracy_7d'] = results['correct_predictions_7d'] / results['total_predictions']
        
        return results
    
    def analyze_confidence_correlation(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze how confidence scores correlate with prediction accuracy.
        
        Args:
            results: Results from calculate_sentiment_accuracy
            
        Returns:
            Confidence analysis results
        """
        detailed_results = results['detailed_results']
        if not detailed_results:
            return {}
        
        df = pd.DataFrame(detailed_results)
        
        # Bin confidence scores
        df['confidence_bin'] = pd.cut(df['confidence_score'], 
                                    bins=[0, 0.3, 0.5, 0.7, 1.0], 
                                    labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
        
        confidence_analysis = {}
        
        for conf_bin in df['confidence_bin'].unique():
            if pd.isna(conf_bin):
                continue
                
            bin_data = df[df['confidence_bin'] == conf_bin]
            
            # Calculate accuracy for this confidence bin
            bin_results = {
                'count': len(bin_data),
                'avg_confidence': bin_data['confidence_score'].mean(),
                'accuracy_1d': 0,
                'accuracy_3d': 0, 
                'accuracy_7d': 0,
                'avg_return_1d': bin_data['forward_1d_return'].mean(),
                'avg_return_3d': bin_data['forward_3d_return'].mean(),
                'avg_return_7d': bin_data['forward_7d_return'].mean()
            }
            
            # Calculate direction accuracy for each time horizon
            for period in ['1d', '3d', '7d']:
                return_col = f'forward_{period}_return'
                if return_col in bin_data.columns:
                    valid_data = bin_data.dropna(subset=[return_col])
                    if len(valid_data) > 0:
                        correct_predictions = sum(
                            (valid_data['predicted_direction'] == 1) & (valid_data[return_col] > 0) |
                            (valid_data['predicted_direction'] == -1) & (valid_data[return_col] < 0)
                        )
                        bin_results[f'accuracy_{period}'] = correct_predictions / len(valid_data)
            
            confidence_analysis[str(conf_bin)] = bin_results
        
        return confidence_analysis
    
    def run_comprehensive_backtest(self, days_back=30) -> Dict[str, Any]:
        """
        Run comprehensive backtesting analysis.
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            Complete backtesting results
        """
        logger.info(f"Starting comprehensive backtest for past {days_back} days")
        
        # Get historical sentiment data
        sentiment_df = self.get_historical_sentiment_data(days_back)
        if sentiment_df.empty:
            logger.warning("No historical sentiment data found")
            return {}
        
        # Get unique symbols
        symbols = sentiment_df['symbol'].unique().tolist()
        logger.info(f"Analyzing {len(symbols)} symbols: {symbols}")
        
        # Get price data
        price_data = self.get_stock_price_data(symbols, days_back)
        if not price_data:
            logger.warning("No price data retrieved")
            return {}
        
        # Calculate accuracy
        accuracy_results = self.calculate_sentiment_accuracy(sentiment_df, price_data)
        
        # Analyze confidence correlation
        confidence_analysis = self.analyze_confidence_correlation(accuracy_results)
        
        # Compile final results
        backtest_results = {
            'summary': {
                'analysis_period_days': days_back,
                'symbols_analyzed': len(symbols),
                'total_predictions': accuracy_results['total_predictions'],
                'accuracy_1d': accuracy_results['accuracy_1d'],
                'accuracy_3d': accuracy_results['accuracy_3d'],
                'accuracy_7d': accuracy_results['accuracy_7d']
            },
            'confidence_analysis': confidence_analysis,
            'detailed_results': accuracy_results['detailed_results'],
            'symbols_analyzed': symbols
        }
        
        logger.info("Backtesting analysis complete")
        return backtest_results
    
    def generate_backtest_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a formatted backtest report.
        
        Args:
            results: Backtesting results
            
        Returns:
            Formatted report string
        """
        if not results:
            return "No backtesting results available."
        
        summary = results['summary']
        confidence_analysis = results.get('confidence_analysis', {})
        
        report = []
        report.append("=" * 80)
        report.append("📊 SENTIMENT ANALYSIS BACKTESTING REPORT")
        report.append("=" * 80)
        
        report.append(f"\n📈 OVERALL PERFORMANCE:")
        report.append(f"   • Analysis Period: {summary['analysis_period_days']} days")
        report.append(f"   • Symbols Analyzed: {summary['symbols_analyzed']}")
        report.append(f"   • Total Predictions: {summary['total_predictions']}")
        report.append(f"   • 1-Day Accuracy: {summary['accuracy_1d']:.1%}")
        report.append(f"   • 3-Day Accuracy: {summary['accuracy_3d']:.1%}")
        report.append(f"   • 7-Day Accuracy: {summary['accuracy_7d']:.1%}")
        
        if confidence_analysis:
            report.append(f"\n🎯 CONFIDENCE LEVEL ANALYSIS:")
            report.append("-" * 60)
            report.append(f"{'Confidence':<12} {'Count':<6} {'1D Acc':<8} {'3D Acc':<8} {'7D Acc':<8} {'Avg 1D Ret':<10}")
            report.append("-" * 60)
            
            for conf_level, data in confidence_analysis.items():
                report.append(f"{conf_level:<12} {data['count']:<6} "
                            f"{data['accuracy_1d']:<8.1%} {data['accuracy_3d']:<8.1%} "
                            f"{data['accuracy_7d']:<8.1%} {data['avg_return_1d']:<10.2%}")
        
        report.append(f"\n💡 KEY INSIGHTS:")
        if summary['accuracy_7d'] > 0.6:
            report.append("   🟢 Strong 7-day predictive power (>60% accuracy)")
        elif summary['accuracy_7d'] > 0.5:
            report.append("   🟡 Moderate 7-day predictive power (50-60% accuracy)")
        else:
            report.append("   🔴 Limited 7-day predictive power (<50% accuracy)")
        
        # Best confidence level
        if confidence_analysis:
            best_conf = max(confidence_analysis.items(), 
                          key=lambda x: x[1].get('accuracy_7d', 0))
            report.append(f"   📊 Best performing confidence level: {best_conf[0]} "
                        f"({best_conf[1].get('accuracy_7d', 0):.1%} 7-day accuracy)")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
