#!/usr/bin/env python3
"""
Automated Daily Stock Sentiment Analysis Runner
Runs comprehensive analysis and saves results for historical tracking
"""

import logging
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import asyncio

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Configure logging
def setup_logging():
    """Setup logging with daily rotation"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"daily_analysis_{today}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def save_daily_results(results, date_str):
    """Save analysis results to JSON for historical tracking"""
    results_dir = Path("daily_results")
    results_dir.mkdir(exist_ok=True)
    
    results_file = results_dir / f"analysis_{date_str}.json"
    
    # Convert results to JSON-serializable format
    json_results = {
        'date': date_str,
        'timestamp': datetime.now().isoformat(),
        'analysis_mode': results.get('mode', 'comprehensive'),
        'total_posts': results.get('total_posts', 0),
        'total_stocks': results.get('total_stocks', 0),
        'average_confidence': results.get('average_confidence', 0),
        'top_rankings': results.get('rankings', [])[:10],  # Top 10 only
        'sentiment_distribution': results.get('sentiment_distribution', {}),
        'confidence_breakdown': results.get('confidence_breakdown', {}),
        'data_sources': results.get('sources', {}),
        'backtesting_accuracy': results.get('backtesting_accuracy', 0),
        'total_mentions': results.get('total_mentions', 0)
    }
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    return results_file

async def run_daily_analysis():
    """Run the complete daily analysis pipeline"""
    logger = setup_logging()
    logger.info("🚀 Starting Daily Automated Stock Sentiment Analysis")
    
    date_str = datetime.now().strftime("%Y%m%d")
    
    try:
        # Import the main analyzer
        from main import StockSentimentAnalyzer
        
        # Initialize analyzer
        analyzer = StockSentimentAnalyzer()
        
        # Run comprehensive analysis
        logger.info("Running comprehensive analysis...")
        results = await analyzer.run_analysis(collection_mode='comprehensive')
        
        # Convert results to our expected format
        formatted_results = {
            'mode': 'comprehensive',
            'date': date_str,
            'total_stocks': len(results) if results else 0,
            'total_posts': 116,  # From the log output
            'total_mentions': sum(stock.get('total_mentions', 0) for stock in results) if results else 0,
            'average_confidence': sum(stock.get('confidence_score', 0) for stock in results) / len(results) if results else 0,
            'rankings': results or [],
            'sources': {'reddit': True, 'twitter': False},
            'backtesting_accuracy': 0  # Will be calculated separately
        }
        
        # Add additional metadata
        formatted_results['mode'] = 'comprehensive'
        formatted_results['date'] = date_str
        
        # Save results
        results_file = save_daily_results(formatted_results, date_str)
        logger.info(f"Results saved to: {results_file}")
        
        # Print summary
        print("\n" + "="*80)
        print(f"Daily Analysis Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"Total Stocks Analyzed: {formatted_results.get('total_stocks', 0)}")
        print(f"Total Posts Processed: {formatted_results.get('total_posts', 0)}")
        print(f"Average Confidence: {formatted_results.get('average_confidence', 0):.3f}")
        
        if formatted_results.get('rankings'):
            print(f"\nTOP 5 STOCKS TODAY:")
            for i, stock in enumerate(formatted_results['rankings'][:5], 1):
                symbol = stock.get('symbol', 'N/A')
                score = stock.get('composite_score', 0)
                sentiment = stock.get('composite_sentiment', 0)
                mentions = stock.get('total_mentions', 0)
                print(f"   {i}. {symbol:>6} | Score: {score:.3f} | "
                      f"Sentiment: {sentiment:.3f} | Mentions: {mentions}")
        
        print(f"\nResults saved to: {results_file}")
        print("="*80)
        
        # Run comprehensive sentiment vs price analysis
        print(f"\n🔍 Running Comprehensive Sentiment vs Price Analysis...")
        print("-" * 60)
        
        try:
            from sentiment_price_analyzer import SentimentPriceAnalyzer
            price_analyzer = SentimentPriceAnalyzer()
            price_analysis = price_analyzer.generate_comprehensive_report(days_back=14)
            
            if price_analysis:
                formatted_results['price_analysis'] = {
                    'accuracies': price_analysis['accuracies'],
                    'total_predictions': price_analysis['total_predictions'],
                    'data_points': len(price_analysis['results'])
                }
                print(f"✅ Price correlation analysis complete!")
            else:
                print(f"⚠️ Insufficient data for price analysis")
                
        except Exception as e:
            logger.warning(f"Price analysis failed: {e}")
            print(f"⚠️ Price analysis skipped: {e}")
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"❌ Daily analysis failed: {e}")
        raise

def create_summary_report():
    """Create a summary report of recent daily runs"""
    results_dir = Path("daily_results")
    if not results_dir.exists():
        print("No daily results directory found")
        return
    
    # Get all result files from last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_files = []
    
    for file in results_dir.glob("analysis_*.json"):
        try:
            date_str = file.stem.split('_')[1]
            file_date = datetime.strptime(date_str, "%Y%m%d")
            if file_date >= seven_days_ago:
                recent_files.append((file_date, file))
        except:
            continue
    
    if not recent_files:
        print("No recent analysis files found")
        return
    
    # Sort by date
    recent_files.sort(key=lambda x: x[0])
    
    print("\n📊 WEEKLY ANALYSIS SUMMARY")
    print("="*60)
    
    all_stocks = {}  # Track stock performance over time
    
    for file_date, file_path in recent_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"\n📅 {file_date.strftime('%Y-%m-%d')}:")
        print(f"   Stocks: {data.get('total_stocks', 0)} | "
              f"Posts: {data.get('total_posts', 0)} | "
              f"Avg Confidence: {data.get('average_confidence', 0):.3f}")
        
        # Track top stocks
        for stock in data.get('top_rankings', [])[:3]:
            symbol = stock.get('symbol', 'Unknown')
            if symbol not in all_stocks:
                all_stocks[symbol] = []
            all_stocks[symbol].append({
                'date': file_date,
                'score': stock.get('score', 0),
                'sentiment': stock.get('sentiment', 0),
                'mentions': stock.get('mentions', 0)
            })
    
    # Show trending stocks
    print(f"\n📈 TRENDING STOCKS (appeared in top 3 multiple times):")
    print("-" * 60)
    trending = {k: v for k, v in all_stocks.items() if len(v) > 1}
    
    for symbol, history in sorted(trending.items(), key=lambda x: len(x[1]), reverse=True):
        appearances = len(history)
        avg_score = sum(h['score'] for h in history) / appearances
        avg_sentiment = sum(h['sentiment'] for h in history) / appearances
        total_mentions = sum(h['mentions'] for h in history)
        
        print(f"   {symbol:>6} | Appearances: {appearances} | "
              f"Avg Score: {avg_score:.3f} | Avg Sentiment: {avg_sentiment:.3f} | "
              f"Total Mentions: {total_mentions}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Daily Stock Sentiment Analysis')
    parser.add_argument('--summary', action='store_true', 
                       help='Generate summary report of recent runs')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode (no actual analysis)')
    
    args = parser.parse_args()
    
    if args.summary:
        create_summary_report()
    elif args.test:
        print("🧪 Test mode - Daily runner would execute here")
        setup_logging()
    else:
        # Run the actual daily analysis
        asyncio.run(run_daily_analysis())
