#!/usr/bin/env python3
"""
Comprehensive Sentiment vs Stock Price Performance Analyzer
Amalgamates historical sentiment data with actual stock price movements
"""

import json
import pandas as pd
import sqlite3
import yfinance as yf
from pathlib import Path
from datetime import datetime, timedelta, date
from collections import defaultdict
import numpy as np

class SentimentPriceAnalyzer:
    """Analyzes correlation between sentiment and actual stock price movements"""
    
    def __init__(self, db_path="data/stock_sentiment.db", results_dir="daily_results"):
        self.db_path = db_path
        self.results_dir = Path(results_dir)
        
    def load_historical_sentiment(self, days_back=30):
        """Load historical sentiment data from daily results and database"""
        print(f"📊 Loading sentiment data from past {days_back} days...")
        
        # Load from daily JSON results
        json_data = self._load_json_sentiment_data(days_back)
        
        # Load from database for more granular data
        db_data = self._load_database_sentiment_data(days_back)
        
        # Combine and deduplicate
        combined_data = self._combine_sentiment_data(json_data, db_data)
        
        print(f"✅ Loaded sentiment data for {len(combined_data)} unique stock-date combinations")
        return combined_data
    
    def _load_json_sentiment_data(self, days_back):
        """Load sentiment data from daily JSON files"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        sentiment_data = []
        
        for json_file in self.results_dir.glob("analysis_*.json"):
            try:
                file_date = datetime.strptime(json_file.stem.split('_')[1], "%Y%m%d")
                if file_date < cutoff_date:
                    continue
                    
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                date_str = file_date.strftime('%Y-%m-%d')
                
                for stock in data.get('top_rankings', []):
                    sentiment_data.append({
                        'date': date_str,
                        'symbol': stock.get('symbol'),
                        'sentiment_score': stock.get('composite_sentiment', 0),
                        'mentions': stock.get('total_mentions', 0),
                        'confidence': stock.get('confidence_score', 0),
                        'composite_score': stock.get('composite_score', 0),
                        'source': 'json'
                    })
                    
            except Exception as e:
                print(f"⚠️ Error loading {json_file}: {e}")
                continue
        
        return sentiment_data
    
    def _load_database_sentiment_data(self, days_back):
        """Load sentiment data from database"""
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT 
                DATE(created_at) as date,
                symbol,
                AVG(sentiment_compound) as sentiment_score,
                SUM(mentions) as mentions,
                COUNT(*) as records
            FROM symbol_sentiment_history 
            WHERE DATE(created_at) >= ?
            GROUP BY DATE(created_at), symbol
            ORDER BY date DESC, symbol
            """
            
            db_data = []
            for row in conn.execute(query, (cutoff_date,)):
                db_data.append({
                    'date': row[0],
                    'symbol': row[1],
                    'sentiment_score': row[2],
                    'mentions': row[3],
                    'confidence': min(row[4] / 10.0, 1.0),  # Rough confidence based on records
                    'composite_score': row[2],  # Use sentiment as composite for DB data
                    'source': 'database'
                })
            
            conn.close()
            return db_data
            
        except Exception as e:
            print(f"⚠️ Error loading database data: {e}")
            return []
    
    def _combine_sentiment_data(self, json_data, db_data):
        """Combine and deduplicate sentiment data from multiple sources"""
        combined = {}
        
        # Prefer JSON data over database data (more complete)
        for item in db_data + json_data:  # DB first, then JSON overwrites
            key = f"{item['date']}_{item['symbol']}"
            combined[key] = item
        
        return list(combined.values())
    
    def get_price_data(self, symbols, days_back=30):
        """Fetch historical price data for symbols"""
        print(f"📈 Fetching price data for {len(symbols)} symbols...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back + 10)  # Extra buffer for price calc
        
        price_data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                
                if not hist.empty:
                    # Calculate daily price changes
                    hist['price_change_1d'] = hist['Close'].pct_change() * 100
                    hist['price_change_3d'] = hist['Close'].pct_change(periods=3) * 100
                    hist['price_change_7d'] = hist['Close'].pct_change(periods=7) * 100
                    
                    price_data[symbol] = hist
                    print(f"  ✅ {symbol}: {len(hist)} days of data")
                else:
                    print(f"  ⚠️ {symbol}: No price data available")
                    
            except Exception as e:
                print(f"  ❌ {symbol}: Error fetching data - {e}")
                continue
        
        return price_data
    
    def analyze_sentiment_price_correlation(self, days_back=30):
        """Comprehensive analysis of sentiment vs price performance"""
        print("🔍 COMPREHENSIVE SENTIMENT VS PRICE ANALYSIS")
        print("=" * 80)
        
        # Load sentiment data
        sentiment_data = self.load_historical_sentiment(days_back)
        if not sentiment_data:
            print("❌ No sentiment data available")
            return None
        
        # Get unique symbols
        symbols = list(set(item['symbol'] for item in sentiment_data))
        print(f"📊 Analyzing {len(symbols)} unique symbols")
        
        # Get price data
        price_data = self.get_price_data(symbols, days_back)
        
        # Combine sentiment and price data
        analysis_results = self._correlate_sentiment_with_prices(sentiment_data, price_data)
        
        return analysis_results
    
    def _correlate_sentiment_with_prices(self, sentiment_data, price_data):
        """Correlate sentiment data with price movements"""
        results = []
        correct_predictions = {'1d': 0, '3d': 0, '7d': 0}
        total_predictions = {'1d': 0, '3d': 0, '7d': 0}
        
        for sentiment_item in sentiment_data:
            symbol = sentiment_item['symbol']
            sentiment_date = datetime.strptime(sentiment_item['date'], '%Y-%m-%d').date()
            
            if symbol not in price_data:
                continue
            
            price_hist = price_data[symbol]
            
            # Find the closest trading day
            trading_dates = [d.date() for d in price_hist.index]
            closest_date = min(trading_dates, key=lambda x: abs((x - sentiment_date).days))
            
            if abs((closest_date - sentiment_date).days) > 3:  # Skip if too far apart
                continue
            
            try:
                price_row = price_hist.loc[price_hist.index.date == closest_date].iloc[0]
                
                sentiment_score = sentiment_item['sentiment_score']
                mentions = sentiment_item['mentions']
                confidence = sentiment_item['confidence']
                
                # Analyze different time horizons
                for period in ['1d', '3d', '7d']:
                    price_change = price_row[f'price_change_{period}']
                    
                    if pd.isna(price_change):
                        continue
                    
                    # Determine if prediction was correct
                    sentiment_bullish = sentiment_score > 0.1
                    sentiment_bearish = sentiment_score < -0.1
                    price_up = price_change > 0
                    
                    prediction_made = sentiment_bullish or sentiment_bearish
                    
                    if prediction_made:
                        total_predictions[period] += 1
                        
                        # Check if prediction was correct
                        if (sentiment_bullish and price_up) or (sentiment_bearish and not price_up):
                            correct_predictions[period] += 1
                
                # Store result
                results.append({
                    'symbol': symbol,
                    'date': sentiment_item['date'],
                    'sentiment_score': sentiment_score,
                    'mentions': mentions,
                    'confidence': confidence,
                    'price_change_1d': price_row.get('price_change_1d', 0),
                    'price_change_3d': price_row.get('price_change_3d', 0),
                    'price_change_7d': price_row.get('price_change_7d', 0),
                    'current_price': price_row['Close']
                })
                
            except Exception as e:
                continue
        
        # Calculate accuracy metrics
        accuracies = {}
        for period in ['1d', '3d', '7d']:
            if total_predictions[period] > 0:
                accuracies[period] = (correct_predictions[period] / total_predictions[period]) * 100
            else:
                accuracies[period] = 0
        
        return {
            'results': results,
            'accuracies': accuracies,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions
        }
    
    def generate_comprehensive_report(self, days_back=30):
        """Generate comprehensive sentiment vs price analysis report"""
        analysis = self.analyze_sentiment_price_correlation(days_back)
        
        if not analysis:
            return
        
        results = analysis['results']
        accuracies = analysis['accuracies']
        total_preds = analysis['total_predictions']
        correct_preds = analysis['correct_predictions']
        
        print(f"\n📊 COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        print(f"Analysis Period: {days_back} days")
        print(f"Total Data Points: {len(results)}")
        
        # Overall accuracy
        print(f"\n🎯 PREDICTION ACCURACY:")
        print("-" * 40)
        for period in ['1d', '3d', '7d']:
            accuracy = accuracies[period]
            total = total_preds[period]
            correct = correct_preds[period]
            print(f"{period.upper()} Accuracy: {accuracy:5.1f}% ({correct}/{total} correct)")
        
        # Top performers by sentiment accuracy
        df = pd.DataFrame(results)
        
        if not df.empty:
            print(f"\n🏆 TOP PERFORMING STOCKS (Sentiment → Price Correlation):")
            print("-" * 60)
            
            # Group by symbol and calculate performance metrics
            symbol_performance = []
            
            for symbol in df['symbol'].unique():
                symbol_data = df[df['symbol'] == symbol]
                
                # Calculate correlation metrics
                pos_sentiment_count = len(symbol_data[symbol_data['sentiment_score'] > 0.1])
                neg_sentiment_count = len(symbol_data[symbol_data['sentiment_score'] < -0.1])
                
                avg_sentiment = symbol_data['sentiment_score'].mean()
                avg_price_change_7d = symbol_data['price_change_7d'].mean()
                total_mentions = symbol_data['mentions'].sum()
                avg_confidence = symbol_data['confidence'].mean()
                
                # Simple correlation check
                correlation_score = 0
                if avg_sentiment > 0.1 and avg_price_change_7d > 0:
                    correlation_score = min(avg_sentiment * avg_price_change_7d, 1.0)
                elif avg_sentiment < -0.1 and avg_price_change_7d < 0:
                    correlation_score = min(abs(avg_sentiment * avg_price_change_7d), 1.0)
                
                symbol_performance.append({
                    'symbol': symbol,
                    'avg_sentiment': avg_sentiment,
                    'avg_price_change_7d': avg_price_change_7d,
                    'total_mentions': total_mentions,
                    'avg_confidence': avg_confidence,
                    'correlation_score': correlation_score,
                    'data_points': len(symbol_data)
                })
            
            # Sort by correlation score
            symbol_performance.sort(key=lambda x: x['correlation_score'], reverse=True)
            
            for i, perf in enumerate(symbol_performance[:10], 1):
                symbol = perf['symbol']
                sentiment = perf['avg_sentiment']
                price_change = perf['avg_price_change_7d']
                mentions = perf['total_mentions']
                confidence = perf['avg_confidence']
                correlation = perf['correlation_score']
                
                print(f"{i:2d}. {symbol:>6} | Sentiment: {sentiment:>6.3f} | "
                      f"7d Price Δ: {price_change:>6.2f}% | "
                      f"Mentions: {mentions:>3} | Confidence: {confidence:.3f}")
        
        # Save detailed results
        self._save_analysis_results(analysis, days_back)
        
        print(f"\n✅ Comprehensive analysis complete!")
        print("=" * 80)
        
        return analysis
    
    def _save_analysis_results(self, analysis, days_back):
        """Save analysis results to JSON file"""
        results_file = f"sentiment_price_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Convert datetime objects to strings for JSON serialization
        serializable_results = []
        for result in analysis['results']:
            serializable_result = result.copy()
            # Convert any numpy types to regular Python types
            for key, value in serializable_result.items():
                if isinstance(value, (np.integer, np.floating)):
                    serializable_result[key] = float(value)
            serializable_results.append(serializable_result)
        
        output_data = {
            'generated_date': datetime.now().isoformat(),
            'analysis_period_days': days_back,
            'total_data_points': len(analysis['results']),
            'accuracies': analysis['accuracies'],
            'total_predictions': analysis['total_predictions'],
            'correct_predictions': analysis['correct_predictions'],
            'detailed_results': serializable_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Detailed results saved to: {results_file}")

def main():
    analyzer = SentimentPriceAnalyzer()
    
    import argparse
    parser = argparse.ArgumentParser(description='Sentiment vs Price Analysis')
    parser.add_argument('--days', type=int, default=30, 
                       help='Number of days to analyze (default: 30)')
    
    args = parser.parse_args()
    
    analyzer.generate_comprehensive_report(days_back=args.days)

if __name__ == "__main__":
    main()
