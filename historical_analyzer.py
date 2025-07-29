#!/usr/bin/env python3
"""
Historical Data Analyzer
Analyzes trends and patterns from daily automated runs
"""

import json
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
# Optional plotting libraries - install with: pip install matplotlib seaborn
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

def load_daily_results():
    """Load all daily results into a DataFrame"""
    results_dir = Path("daily_results")
    if not results_dir.exists():
        return None
    
    all_data = []
    
    for file in results_dir.glob("analysis_*.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            
            # Extract key metrics
            base_metrics = {
                'date': data.get('date'),
                'timestamp': data.get('timestamp'),
                'total_posts': data.get('total_posts', 0),
                'total_stocks': data.get('total_stocks', 0),
                'average_confidence': data.get('average_confidence', 0),
                'total_mentions': data.get('total_mentions', 0),
                'backtesting_accuracy': data.get('backtesting_accuracy', 0)
            }
            
            # Add top stock data
            rankings = data.get('top_rankings', [])
            for i, stock in enumerate(rankings[:5], 1):
                base_metrics[f'top_{i}_symbol'] = stock.get('symbol', '')
                base_metrics[f'top_{i}_score'] = stock.get('score', 0)
                base_metrics[f'top_{i}_sentiment'] = stock.get('sentiment', 0)
                base_metrics[f'top_{i}_mentions'] = stock.get('mentions', 0)
            
            all_data.append(base_metrics)
            
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue
    
    if not all_data:
        return None
    
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    return df.sort_values('date')

def analyze_stock_trends():
    """Analyze which stocks appear most frequently in top rankings"""
    df = load_daily_results()
    if df is None:
        print("No daily results found")
        return
    
    print("📊 STOCK TREND ANALYSIS")
    print("="*60)
    
    # Count appearances in top 5
    stock_appearances = {}
    stock_scores = {}
    
    for _, row in df.iterrows():
        date = row['date'].strftime('%Y-%m-%d')
        for i in range(1, 6):
            symbol = row.get(f'top_{i}_symbol', '')
            score = row.get(f'top_{i}_score', 0)
            
            if symbol and symbol.strip():
                if symbol not in stock_appearances:
                    stock_appearances[symbol] = []
                    stock_scores[symbol] = []
                
                stock_appearances[symbol].append(date)
                stock_scores[symbol].append(score)
    
    # Sort by frequency
    frequent_stocks = sorted(stock_appearances.items(), 
                           key=lambda x: len(x[1]), reverse=True)
    
    print(f"\n🏆 Most Frequently Ranked Stocks:")
    print("-" * 60)
    for symbol, dates in frequent_stocks[:10]:
        appearances = len(dates)
        avg_score = sum(stock_scores[symbol]) / len(stock_scores[symbol])
        print(f"{symbol:>6} | Appearances: {appearances:>2} | "
              f"Avg Score: {avg_score:.3f} | "
              f"Latest: {dates[-1]}")
    
    return frequent_stocks

def analyze_daily_patterns():
    """Analyze patterns in daily analysis results"""
    df = load_daily_results()
    if df is None:
        print("No daily results found")
        return
    
    print(f"\n📈 DAILY PATTERN ANALYSIS")
    print("="*60)
    
    print(f"Analysis Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"Total Days: {len(df)}")
    
    # Basic statistics
    print(f"\n📊 METRICS SUMMARY:")
    print("-" * 60)
    print(f"Avg Posts per Day: {df['total_posts'].mean():.1f}")
    print(f"Avg Stocks per Day: {df['total_stocks'].mean():.1f}")
    print(f"Avg Confidence: {df['average_confidence'].mean():.3f}")
    print(f"Avg Total Mentions: {df['total_mentions'].mean():.1f}")
    
    # Trends
    if len(df) > 1:
        posts_trend = "📈" if df['total_posts'].iloc[-1] > df['total_posts'].iloc[0] else "📉"
        confidence_trend = "📈" if df['average_confidence'].iloc[-1] > df['average_confidence'].iloc[0] else "📉"
        
        print(f"\n📊 TRENDS:")
        print("-" * 60)
        print(f"Posts Volume: {posts_trend}")
        print(f"Confidence: {confidence_trend}")
    
    return df

def create_historical_report():
    """Create a comprehensive historical analysis report"""
    print("📋 COMPREHENSIVE HISTORICAL ANALYSIS REPORT")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load and analyze data
    df = analyze_daily_patterns()
    frequent_stocks = analyze_stock_trends()
    
    if df is not None and len(df) > 0:
        # Recent performance
        print(f"\n🔍 RECENT PERFORMANCE (Last 7 Days):")
        print("-" * 60)
        recent_df = df.tail(7)
        
        for _, row in recent_df.iterrows():
            date = row['date'].strftime('%Y-%m-%d')
            posts = row['total_posts']
            stocks = row['total_stocks']
            confidence = row['average_confidence']
            top_stock = row.get('top_1_symbol', 'N/A')
            top_score = row.get('top_1_score', 0)
            
            print(f"{date} | Posts: {posts:>3} | Stocks: {stocks:>2} | "
                  f"Confidence: {confidence:.3f} | Top: {top_stock} ({top_score:.3f})")
    
    print(f"\n✅ Historical analysis complete!")
    print("="*80)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Historical Data Analysis')
    parser.add_argument('--trends', action='store_true',
                       help='Analyze stock trends only')
    parser.add_argument('--patterns', action='store_true', 
                       help='Analyze daily patterns only')
    parser.add_argument('--full', action='store_true',
                       help='Full historical report (default)')
    
    args = parser.parse_args()
    
    if args.trends:
        analyze_stock_trends()
    elif args.patterns:
        analyze_daily_patterns()
    else:
        create_historical_report()
