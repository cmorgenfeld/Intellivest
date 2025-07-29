"""
Run backtesting analysis to validate sentiment predictions against actual stock price movements.
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.analysis.backtester import SentimentBacktester


def main():
    """Run backtesting analysis."""
    print("📊 Starting Sentiment Analysis Backtesting...")
    print("This will analyze how well our sentiment predictions correlate with actual price movements.\n")
    
    # Check if we need to install yfinance
    try:
        import yfinance
        print("✅ yfinance available for price data")
    except ImportError:
        print("❌ yfinance not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
        print("✅ yfinance installed")
    
    # Initialize backtester
    backtester = SentimentBacktester()
    
    # Run comprehensive backtest
    print("🔍 Analyzing historical sentiment vs price movements...")
    results = backtester.run_comprehensive_backtest(days_back=30)
    
    if not results:
        print("❌ No backtesting data available.")
        print("💡 Run some sentiment analysis first to generate historical data:")
        print("   python run_comprehensive_analysis.py")
        return
    
    # Generate and display report
    report = backtester.generate_backtest_report(results)
    print(report)
    
    # Additional insights
    summary = results['summary']
    confidence_analysis = results.get('confidence_analysis', {})
    
    print("\n🔬 DETAILED ANALYSIS:")
    
    # Show accuracy by time horizon
    accuracies = [
        ("1-Day", summary['accuracy_1d']),
        ("3-Day", summary['accuracy_3d']), 
        ("7-Day", summary['accuracy_7d'])
    ]
    
    print(f"\n📈 Prediction Accuracy by Time Horizon:")
    for period, accuracy in accuracies:
        if accuracy > 0.6:
            status = "🟢 Strong"
        elif accuracy > 0.5:
            status = "🟡 Moderate"
        else:
            status = "🔴 Weak"
        print(f"   {period}: {accuracy:.1%} {status}")
    
    # Show confidence level insights
    if confidence_analysis:
        print(f"\n🎯 Confidence Level Insights:")
        for level, data in confidence_analysis.items():
            avg_7d_acc = data.get('accuracy_7d', 0)
            avg_return = data.get('avg_return_7d', 0)
            count = data.get('count', 0)
            
            print(f"   {level} Confidence ({count} predictions):")
            print(f"     • 7-day accuracy: {avg_7d_acc:.1%}")
            print(f"     • Average 7-day return: {avg_return:.2%}")
    
    # Trading strategy insights
    print(f"\n💰 TRADING STRATEGY IMPLICATIONS:")
    best_accuracy = max(summary['accuracy_1d'], summary['accuracy_3d'], summary['accuracy_7d'])
    
    if best_accuracy > 0.65:
        print("   🚀 Strong predictive power - Consider systematic trading")
        print("   💡 Focus on high-confidence predictions for better results")
    elif best_accuracy > 0.55:
        print("   📊 Moderate predictive power - Use as one factor among many")
        print("   ⚖️  Combine with technical analysis and risk management")
    else:
        print("   ⚠️  Limited predictive power - Use with extreme caution")
        print("   🔍 Consider improving sentiment analysis or data sources")
    
    # Show symbols with most data
    symbols = results.get('symbols_analyzed', [])
    if symbols:
        print(f"\n📝 Symbols in Analysis: {', '.join(symbols)}")
    
    print(f"\n🔄 Next Steps:")
    print("   • Run more sentiment analysis to increase data points")
    print("   • Experiment with different confidence thresholds")
    print("   • Consider combining sentiment with technical indicators")
    print("   • Monitor real-time predictions and track performance")


if __name__ == "__main__":
    main()
