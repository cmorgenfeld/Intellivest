#!/usr/bin/env python3
"""
Weekly Comprehensive Analysis Report
Combines sentiment analysis, backtesting, and price correlation
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

def run_weekly_comprehensive_analysis():
    """Generate a comprehensive weekly analysis report"""
    print("📊 WEEKLY COMPREHENSIVE ANALYSIS REPORT")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Historical sentiment analysis
    print("1️⃣ HISTORICAL SENTIMENT TRENDS")
    print("-" * 40)
    subprocess.run(["python", "historical_analyzer.py", "--patterns"])
    print()
    
    # 2. Stock trending analysis
    print("2️⃣ STOCK TRENDING ANALYSIS")
    print("-" * 40)
    subprocess.run(["python", "historical_analyzer.py", "--trends"])
    print()
    
    # 3. Sentiment vs Price Correlation (7 days)
    print("3️⃣ SENTIMENT VS PRICE CORRELATION (7 days)")
    print("-" * 50)
    subprocess.run(["python", "sentiment_price_analyzer.py", "--days", "7"])
    print()
    
    # 4. Extended Price Correlation (14 days)
    print("4️⃣ EXTENDED PRICE CORRELATION (14 days)")
    print("-" * 50) 
    subprocess.run(["python", "sentiment_price_analyzer.py", "--days", "14"])
    print()
    
    # 5. Backtesting validation
    print("5️⃣ BACKTESTING VALIDATION")
    print("-" * 30)
    subprocess.run(["python", "demo_backtesting.py"])
    print()
    
    # 6. Weekly summary
    print("6️⃣ WEEKLY DATA SUMMARY")
    print("-" * 30)
    subprocess.run(["python", "automated_daily_runner.py", "--summary"])
    
    print("\n" + "=" * 80)
    print("✅ WEEKLY COMPREHENSIVE ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("📁 Generated Files:")
    print("   • sentiment_price_analysis_YYYYMMDD.json - Price correlation data")
    print("   • Historical trends and patterns displayed above")
    print("   • Backtesting accuracy validation")
    print()
    print("🎯 Key Metrics to Track:")
    print("   • Prediction accuracy trends (improving over time?)")
    print("   • Most frequently mentioned stocks")
    print("   • Sentiment vs actual price correlation")
    print("   • Confidence levels and their accuracy")

if __name__ == "__main__":
    run_weekly_comprehensive_analysis()
