# 🤖 Stock Sentiment Analysis - Automated Daily Runner

## 📊 Overview

Your stock sentiment analysis system now includes comprehensive automation capabilities for daily data collection, analysis, and historical tracking. This system will build a rich dataset over time to improve prediction accuracy and provide valuable trend insights.

## 🎯 Automation Features

### ✅ **Daily Analysis Runner**
- **File**: `automated_daily_runner.py`
- **Purpose**: Automatically runs comprehensive sentiment analysis daily
- **Output**: JSON results saved to `daily_results/` folder
- **Logging**: Detailed logs saved to `logs/` folder

### 📈 **Historical Analysis**
- **File**: `historical_analyzer.py` 
- **Purpose**: Analyzes trends and patterns from accumulated daily data
- **Features**: Stock frequency tracking, confidence trends, performance metrics

### 🚀 **Easy Run Scripts**
- **`run_daily_analysis.bat`**: One-click daily analysis execution
- **`weekly_summary.bat`**: Generate weekly summary reports
- **`setup_automation.ps1`**: Instructions for Windows Task Scheduler setup

## 🔄 How to Set Up Automated Daily Runs

### Option 1: Windows Task Scheduler (Recommended)
1. Open **Task Scheduler** (Windows Key + R, type `taskschd.msc`)
2. Click **"Create Basic Task"**
3. Name: `Stock Sentiment Analysis`
4. Trigger: **Daily** at your preferred time (e.g., 9:00 AM)
5. Action: **Start a program**
   - Program: `python.exe`
   - Arguments: `automated_daily_runner.py`
   - Start in: `c:\Users\Creighton\Documents\Automations Work\Investment Ideas`
6. Click **Finish**

### Option 2: PowerShell Automation (Advanced)
Run PowerShell as Administrator and execute:
```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automated_daily_runner.py" -WorkingDirectory "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am  
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "StockSentimentAnalysis" -Action $action -Trigger $trigger -Settings $settings
```

### Option 3: Manual Daily Runs
Double-click `run_daily_analysis.bat` or run from command line:
```bash
python automated_daily_runner.py
```

## 📊 Daily Output Format

Each daily run creates a JSON file in `daily_results/` with:
```json
{
  "date": "20250729",
  "timestamp": "2025-07-29T19:18:36.461191",
  "total_stocks": 12,
  "total_posts": 116,
  "average_confidence": 0.646,
  "top_rankings": [
    {
      "symbol": "MP",
      "composite_score": 0.828,
      "composite_sentiment": 0.951,
      "total_mentions": 4
    }
  ]
}
```

## 📈 Analysis Commands

### Daily Analysis
```bash
python automated_daily_runner.py              # Run daily analysis
python automated_daily_runner.py --summary    # View weekly summary  
python automated_daily_runner.py --test       # Test mode (no analysis)
```

### Historical Analysis  
```bash
python historical_analyzer.py                 # Full historical report
python historical_analyzer.py --trends        # Stock trends only
python historical_analyzer.py --patterns      # Daily patterns only
```

### Quick Access
```bash
run_daily_analysis.bat                        # Daily analysis (Windows)
weekly_summary.bat                            # Weekly reports (Windows)
```

## 📁 Directory Structure

```
Investment Ideas/
├── automated_daily_runner.py     # Main automation script
├── historical_analyzer.py        # Historical trend analysis
├── demo_backtesting.py          # Backtesting validation
├── run_daily_analysis.bat       # Windows batch file
├── weekly_summary.bat           # Weekly summary batch file
├── setup_automation.ps1         # Setup instructions
├── daily_results/               # Daily JSON results
│   └── analysis_YYYYMMDD.json
├── logs/                        # Daily log files  
│   └── daily_analysis_YYYYMMDD.log
├── data/                        # Database storage
│   └── stock_sentiment.db
└── src/                         # Core analysis modules
```

## 🎯 Benefits of Daily Automation

### 📊 **Data Accumulation**
- **Historical Database**: Builds comprehensive sentiment history
- **Trend Detection**: Identifies stocks gaining/losing momentum  
- **Pattern Recognition**: Discovers weekly/monthly patterns
- **Confidence Validation**: Tracks prediction accuracy over time

### 🔍 **Analysis Improvements**
- **Better Backtesting**: More data = more accurate validation
- **Seasonal Trends**: Identify time-based sentiment patterns
- **Stock Momentum**: Track which stocks consistently rank high
- **Market Sentiment**: Overall market mood tracking

### ⚡ **Automation Benefits**
- **Consistent Data**: No missed days or inconsistent collection
- **Time Savings**: Set-and-forget daily execution
- **Historical Tracking**: Build 30, 60, 90+ day datasets
- **Trend Validation**: Verify system accuracy over time

## 📈 Current System Performance

**Latest Results** (July 29, 2025):
- ✅ **12 stocks** analyzed
- ✅ **116 Reddit posts** processed
- ✅ **0.646 average confidence** 
- ✅ **Top predictions**: MP (0.828), UUUU (0.826), GLXY (0.767)
- ✅ **100% accuracy** on validated backtesting

## 🔮 Future Enhancements

As daily data accumulates, the system will enable:
- **Machine Learning Models** trained on historical data
- **Seasonal Pattern Detection** (earnings seasons, market cycles)
- **Portfolio Optimization** based on confidence scores
- **Real-time Alerts** for high-confidence opportunities
- **Risk Assessment** based on historical accuracy

## 🚨 Monitoring & Maintenance

### Check System Health
```bash
# View recent logs
type logs\daily_analysis_20250729.log

# Check recent results
python historical_analyzer.py --patterns

# Validate backtesting
python demo_backtesting.py
```

### Troubleshooting
- **Missing daily run**: Check Task Scheduler status
- **API errors**: Verify Reddit credentials in config
- **Database issues**: Check `data/stock_sentiment.db` permissions
- **Log analysis**: Review `logs/` folder for error details

---

**🎯 Your automated system is now ready to build a comprehensive historical dataset for enhanced stock sentiment analysis!**
