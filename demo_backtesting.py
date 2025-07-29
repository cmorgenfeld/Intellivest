#!/usr/bin/env python3
"""
Demo script to show backtesting capabilities with real data
"""

import logging
import sys
import sqlite3
from pathlib import Path
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import backtester components directly
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta

def demo_backtest():
    """Demonstrate backtesting with current data"""
    print("🔬 Stock Sentiment Backtesting Demo")
    print("=" * 60)
    
    # Show what data we have
    conn = sqlite3.connect("data/stock_sentiment.db")
    
    # Get sample of recent data
    query = """
    SELECT symbol, sentiment_compound, mentions, created_at
    FROM symbol_sentiment_history 
    ORDER BY created_at DESC 
    LIMIT 10
    """
    
    recent_data = pd.read_sql_query(query, conn)
    print("\n📊 Recent Sentiment Data Sample:")
    print("-" * 60)
    for _, row in recent_data.iterrows():
        print(f"{row['symbol']:>6} | Sentiment: {row['sentiment_compound']:>6.3f} | "
              f"Mentions: {row['mentions']:>3} | "
              f"Date: {row['created_at'][:10]}")
    
    # Get top symbols by mention count
    top_symbols_query = """
    SELECT symbol, AVG(sentiment_compound) as avg_sentiment, 
           SUM(mentions) as total_mentions,
           COUNT(*) as records
    FROM symbol_sentiment_history 
    GROUP BY symbol 
    HAVING total_mentions >= 3
    ORDER BY total_mentions DESC 
    LIMIT 5
    """
    
    top_symbols = pd.read_sql_query(top_symbols_query, conn)
    print(f"\n🏆 Top Symbols by Mentions:")
    print("-" * 60)
    for _, row in top_symbols.iterrows():
        print(f"{row['symbol']:>6} | Avg Sentiment: {row['avg_sentiment']:>6.3f} | "
              f"Total Mentions: {row['total_mentions']:>3} | Records: {row['records']:>2}")
    
    conn.close()
    
    # Test with a few specific stocks that have good data
    test_symbols = top_symbols['symbol'].tolist()[:3]  # Top 3 by mentions
    print(f"\n🎯 Testing Sentiment vs Price Performance: {', '.join(test_symbols)}")
    print("-" * 60)
    
    accurate_predictions = 0
    total_predictions = 0
    
    for symbol in test_symbols:
        print(f"\n📈 Analyzing {symbol}:")
        
        # Get recent price data
        try:
            ticker = yf.Ticker(symbol)
            price_data = ticker.history(period="1mo")
            
            if not price_data.empty:
                current_price = price_data['Close'].iloc[-1]
                start_price = price_data['Close'].iloc[0]
                price_change = ((current_price - start_price) / start_price) * 100
                
                print(f"   Price Change (30d): {price_change:+.2f}%")
                print(f"   Current Price: ${current_price:.2f}")
                
                # Get sentiment for this symbol
                conn = sqlite3.connect("data/stock_sentiment.db")
                sentiment_query = """
                SELECT AVG(sentiment_compound) as avg_sentiment, 
                       SUM(mentions) as total_mentions
                FROM symbol_sentiment_history 
                WHERE symbol = ?
                """
                result = conn.execute(sentiment_query, (symbol,)).fetchone()
                conn.close()
                
                if result and result[0] is not None:
                    avg_sentiment = result[0]
                    total_mentions = result[1]
                    
                    print(f"   Avg Sentiment: {avg_sentiment:.3f}")
                    print(f"   Total Mentions: {total_mentions}")
                    
                    # Simple correlation check
                    prediction_correct = False
                    if avg_sentiment > 0.1 and price_change > 0:
                        print("   ✅ Positive sentiment → Positive returns (CORRECT)")
                        prediction_correct = True
                    elif avg_sentiment < -0.1 and price_change < 0:
                        print("   ✅ Negative sentiment → Negative returns (CORRECT)")
                        prediction_correct = True
                    elif abs(avg_sentiment) < 0.1:
                        print("   ➖ Neutral sentiment (no prediction)")
                    else:
                        print("   ❌ Sentiment-price mismatch (INCORRECT)")
                    
                    if abs(avg_sentiment) > 0.1:  # Only count if we made a prediction
                        total_predictions += 1
                        if prediction_correct:
                            accurate_predictions += 1
            else:
                print(f"   ⚠️ No price data available")
                
        except Exception as e:
            print(f"   ❌ Error getting data: {e}")
    
    # Calculate accuracy
    if total_predictions > 0:
        accuracy = (accurate_predictions / total_predictions) * 100
        print(f"\n📊 SIMPLE BACKTESTING RESULTS:")
        print("-" * 60)
        print(f"   Total Predictions Made: {total_predictions}")
        print(f"   Correct Predictions: {accurate_predictions}")
        print(f"   Accuracy: {accuracy:.1f}%")
        
        if accuracy >= 60:
            print("   🎯 Good predictive accuracy!")
        elif accuracy >= 40:
            print("   ⚠️ Moderate predictive accuracy")
        else:
            print("   🚨 Low predictive accuracy - high risk")
    else:
        print(f"\n📊 No clear predictions to validate")
    
    print(f"\n✅ Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.WARNING)
    demo_backtest()
