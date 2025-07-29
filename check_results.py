#!/usr/bin/env python3
"""
Quick script to check what was scraped from Reddit.
"""

import sqlite3
import sys
sys.path.append('src')

def check_results():
    """Check what was scraped from Reddit."""
    try:
        conn = sqlite3.connect('data/stock_sentiment.db')
        cursor = conn.cursor()
        
        # Check total posts
        cursor.execute('SELECT COUNT(*) FROM reddit_posts')
        total_posts = cursor.fetchone()[0]
        print(f"📊 Total Reddit posts scraped: {total_posts}")
        
        # Check posts with stock symbols
        cursor.execute('SELECT symbols, title, sentiment_compound FROM reddit_posts WHERE symbols != ""')
        results = cursor.fetchall()
        
        print(f"\n🎯 Posts mentioning stocks: {len(results)}")
        print("-" * 80)
        
        for symbols, title, sentiment in results:
            print(f"Symbols: {symbols}")
            print(f"Title: {title[:70]}...")
            print(f"Sentiment: {sentiment:.3f}")
            print("-" * 40)
        
        # Check all symbol mentions
        cursor.execute('SELECT symbols FROM reddit_posts WHERE symbols != ""')
        all_symbols = []
        for (symbols_str,) in cursor.fetchall():
            if symbols_str:
                all_symbols.extend(symbols_str.split(','))
        
        if all_symbols:
            from collections import Counter
            symbol_counts = Counter(all_symbols)
            print(f"\n📈 Stock symbol mentions:")
            for symbol, count in symbol_counts.most_common():
                print(f"  ${symbol}: {count} mentions")
        else:
            print("\n❌ No stock symbols found in any posts")
            
            # Show some sample titles to see what was scraped
            cursor.execute('SELECT title FROM reddit_posts LIMIT 5')
            sample_titles = cursor.fetchall()
            print("\n📝 Sample post titles:")
            for (title,) in sample_titles:
                print(f"  • {title}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_results()
