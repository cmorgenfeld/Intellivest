"""
Enhanced analysis script with different collection modes for comprehensive data gathering.
"""

import asyncio
import logging
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.main import StockSentimentAnalyzer
from src.utils.helpers import setup_directories

try:
    from src.analysis.backtester import SentimentBacktester
    BACKTESTING_AVAILABLE = True
except ImportError:
    BACKTESTING_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def run_comprehensive_analysis(mode="comprehensive"):
    """Run comprehensive sentiment analysis with enhanced data collection."""
    logger.info(f"🚀 Starting Enhanced Stock Sentiment Analysis - {mode.upper()} mode")
    
    try:
        # Setup necessary directories
        setup_directories()
        
        # Initialize and run analyzer
        analyzer = StockSentimentAnalyzer()
        rankings = await analyzer.run_analysis(collection_mode=mode)
        
        # Display enhanced results
        print("\n" + "="*80)
        print(f"🏆 COMPREHENSIVE STOCK RANKINGS ({mode.upper()} MODE)")
        print("="*80)
        
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   • Total stocks analyzed: {len(rankings)}")
        if rankings:
            total_mentions = sum(stock['total_mentions'] for stock in rankings)
            avg_confidence = sum(stock['confidence_score'] for stock in rankings) / len(rankings)
            print(f"   • Total stock mentions: {total_mentions}")
            print(f"   • Average confidence: {avg_confidence:.3f}")
        
        print(f"\n🥇 TOP 15 STOCK RANKINGS:")
        print("-" * 80)
        print(f"{'Rank':<4} {'Symbol':<8} {'Score':<8} {'Sentiment':<10} {'Mentions':<8} {'Confidence':<10} {'Engagement':<12}")
        print("-" * 80)
        
        for stock in rankings[:15]:
            reddit_engagement = stock.get('reddit_engagement', 0)
            print(f"{stock['rank']:<4} {stock['symbol']:<8} "
                  f"{stock['composite_score']:<8.3f} {stock['composite_sentiment']:<10.3f} "
                  f"{stock['total_mentions']:<8} {stock['confidence_score']:<10.3f} "
                  f"{reddit_engagement:<12.0f}")
        
        # Show confidence breakdown
        if rankings:
            high_confidence = [s for s in rankings if s['confidence_score'] >= 0.7]
            medium_confidence = [s for s in rankings if 0.4 <= s['confidence_score'] < 0.7]
            low_confidence = [s for s in rankings if s['confidence_score'] < 0.4]
            
            print(f"\n📈 CONFIDENCE BREAKDOWN:")
            print(f"   🟢 High Confidence (≥0.7): {len(high_confidence)} stocks")
            print(f"   🟡 Medium Confidence (0.4-0.7): {len(medium_confidence)} stocks") 
            print(f"   🔴 Low Confidence (<0.4): {len(low_confidence)} stocks")
        
        # Show sentiment distribution
        if rankings:
            very_bullish = [s for s in rankings if s['composite_sentiment'] >= 0.5]
            bullish = [s for s in rankings if 0.1 <= s['composite_sentiment'] < 0.5]
            neutral = [s for s in rankings if -0.1 <= s['composite_sentiment'] < 0.1]
            bearish = [s for s in rankings if s['composite_sentiment'] < -0.1]
            
            print(f"\n💹 SENTIMENT DISTRIBUTION:")
            print(f"   🚀 Very Bullish (≥0.5): {len(very_bullish)} stocks")
            print(f"   📈 Bullish (0.1-0.5): {len(bullish)} stocks")
            print(f"   ➖ Neutral (-0.1-0.1): {len(neutral)} stocks")
            print(f"   📉 Bearish (<-0.1): {len(bearish)} stocks")
        
        print("\n" + "="*80)
        print("✅ Comprehensive analysis complete!")
        print(f"📊 {len(rankings)} stocks analyzed and ranked")
        print("💾 All data stored in database for historical tracking")
        print("🔄 Run again to see how sentiment changes over time")
        print("="*80)
        
        # Run backtesting if available and we have historical data
        if BACKTESTING_AVAILABLE and len(rankings) > 0:
            print("\n📊 Running Historical Backtesting Analysis...")
            try:
                backtester = SentimentBacktester()
                backtest_results = backtester.run_comprehensive_backtest(days_back=30)
                
                if backtest_results:
                    print("\n" + backtester.generate_backtest_report(backtest_results))
                    
                    # Show expectation tempering insights
                    summary = backtest_results['summary']
                    print(f"\n🎯 EXPECTATION TEMPERING:")
                    print(f"   • Based on {summary['total_predictions']} historical predictions")
                    print(f"   • 7-day accuracy: {summary['accuracy_7d']:.1%}")
                    
                    if summary['accuracy_7d'] > 0.6:
                        print("   ✅ Historical performance suggests reliable predictions")
                    elif summary['accuracy_7d'] > 0.5:
                        print("   ⚠️  Moderate historical accuracy - use with other indicators")
                    else:
                        print("   🚨 Limited historical accuracy - high risk predictions")
                        
                else:
                    print("   📝 Insufficient historical data for backtesting")
                    print("   💡 Run analysis regularly to build backtesting dataset")
                    
            except Exception as e:
                logger.warning(f"Backtesting failed: {e}")
                print("   ⚠️  Backtesting unavailable (may need: pip install yfinance)")
        
        return rankings
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        raise


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description='Run stock sentiment analysis')
    parser.add_argument('--mode', 
                       choices=['normal', 'extended', 'comprehensive'],
                       default='comprehensive',
                       help='Collection mode: normal (100 posts), extended (300 posts), comprehensive (500 posts)')
    
    args = parser.parse_args()
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Run the analysis
    asyncio.run(run_comprehensive_analysis(args.mode))


if __name__ == "__main__":
    main()
