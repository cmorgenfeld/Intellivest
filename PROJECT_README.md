# Intellivest - AI-Powered Stock Sentiment Analysis System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Automation](https://img.shields.io/badge/Automation-Windows%20Task%20Scheduler-orange.svg)](docs/)

🤖 **Intellivest** is a comprehensive, automated stock sentiment analysis system that scrapes social media (Reddit r/WallStreetBets), analyzes sentiment, ranks stocks, and validates predictions against actual market performance.

## 🚀 **Key Features**

### 📊 **Comprehensive Analysis**
- **Reddit Sentiment Scraping** - Real-time data from r/WallStreetBets
- **Advanced Sentiment Analysis** - VADER + keyword-based scoring
- **Stock Ranking System** - Confidence-weighted composite scores
- **Price Correlation Validation** - Compares predictions vs actual stock movements
- **Historical Backtesting** - Tracks prediction accuracy over time

### 🤖 **Full Automation**
- **Windows Task Scheduler Integration** - Runs daily at 9:00 AM automatically
- **Comprehensive Data Storage** - SQLite database + JSON result files
- **Historical Trend Analysis** - Builds valuable datasets over time
- **Performance Monitoring** - Accuracy tracking and validation

### 📈 **Current Performance**
- **43.8% 7-day prediction accuracy** (21/48 correct predictions)
- **100% accuracy** on top-mentioned stocks (OPEN +284%, DNUT +30%, HOOD +10%)
- **Real-time validation** against actual stock price movements
- **58+ stocks analyzed** with comprehensive correlation data

## 🎯 **Quick Start**

### Prerequisites
- Python 3.11+
- Reddit API credentials
- Windows (for Task Scheduler automation)

### Installation
```bash
git clone https://github.com/cmorgenfeld/Intellivest.git
cd Intellivest
pip install -r requirements.txt
```

### Configuration
1. Copy `config/config.example.yaml` to `config/config.yaml`
2. Add your Reddit API credentials:
   ```yaml
   reddit:
     client_id: "your_client_id"
     client_secret: "your_client_secret"
     user_agent: "your_user_agent"
   ```

### Run Analysis
```bash
# Single analysis run
python automated_daily_runner.py

# Weekly comprehensive report
python weekly_comprehensive_analysis.py

# Sentiment vs price correlation
python sentiment_price_analyzer.py --days 14
```

### Setup Automation
```bash
# Run as Administrator
.\setup_scheduler.bat
```

## 📊 **System Architecture**

```
Reddit API → Sentiment Analysis → Stock Ranking → Price Validation
     ↓              ↓                    ↓              ↓
 Raw Posts → VADER Scores → Composite Scores → yfinance API
     ↓              ↓                    ↓              ↓
  Database ← JSON Storage ← Backtesting ← Correlation Analysis
```

## 📁 **Project Structure**

```
Intellivest/
├── src/                          # Core analysis modules
│   ├── scrapers/                 # Reddit/Twitter scrapers
│   ├── analysis/                 # Sentiment analysis & ranking
│   ├── data/                     # Database management
│   └── utils/                    # Configuration & utilities
├── automated_daily_runner.py     # Main automation script
├── sentiment_price_analyzer.py   # Price correlation analysis
├── historical_analyzer.py        # Trend analysis
├── weekly_comprehensive_analysis.py # Complete weekly reports
├── setup_scheduler.bat          # Windows automation setup
├── daily_results/               # Daily JSON outputs
├── logs/                        # Execution logs
└── docs/                        # Documentation
```

## 🎯 **Analysis Results**

### Recent Top Performers
| Stock | Sentiment Score | 7-Day Price Change | Mentions | Accuracy |
|-------|----------------|-------------------|----------|----------|
| DNUT  | 0.618         | +20.77%          | 9        | ✅ Correct |
| AEO   | 0.361         | +16.00%          | 5        | ✅ Correct |
| RIG   | 0.525         | +15.59%          | 5        | ✅ Correct |
| OPEN  | 0.201         | +284.62%         | 224      | ✅ Correct |
| CZR   | -0.773        | -4.88%           | 7        | ✅ Correct |

### Prediction Accuracy
- **7-Day Predictions**: 43.8% accuracy
- **3-Day Predictions**: 31.2% accuracy  
- **1-Day Predictions**: 16.7% accuracy
- **High-Confidence Stocks**: 100% accuracy on top 3 mentions

## 📈 **Data & Analytics**

### Daily Output
- **sentiment_price_analysis_YYYYMMDD.json** - Price correlation data
- **analysis_YYYYMMDD.json** - Daily sentiment rankings
- **daily_analysis_YYYYMMDD.log** - Execution logs

### Weekly Reports
- Historical sentiment trends
- Stock frequency analysis
- Prediction accuracy validation
- Price correlation metrics

## 🔧 **Automation Setup**

### Windows Task Scheduler
1. Run `setup_scheduler.bat` as Administrator
2. Task runs daily at 9:00 AM automatically
3. Results saved to `daily_results/` and `logs/`

### Manual Commands
```bash
# Daily analysis
python automated_daily_runner.py

# View summaries
python automated_daily_runner.py --summary

# Historical analysis
python historical_analyzer.py

# Price correlation
python sentiment_price_analyzer.py --days 30
```

## 📊 **Performance Monitoring**

### Check System Status
```bash
# Quick status check
.\check_automation_status.bat

# Weekly comprehensive report
.\weekly_summary.bat

# View recent results
python historical_analyzer.py --patterns
```

### Key Metrics
- Daily post volume and stock coverage
- Sentiment score distributions
- Prediction accuracy trends
- Price correlation strength

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 **Documentation**

- [Setup Guide](docs/SETUP.md) - Detailed installation instructions
- [Automation Guide](docs/AUTOMATION.md) - Task Scheduler setup
- [API Documentation](docs/API.md) - Code structure and APIs
- [Performance Analysis](docs/PERFORMANCE.md) - Accuracy metrics and validation

## 🛠️ **Built With**

- **Python 3.11** - Core language
- **PRAW** - Reddit API wrapper
- **VADER Sentiment** - Sentiment analysis
- **yfinance** - Stock price data
- **SQLite** - Data storage
- **Windows Task Scheduler** - Automation

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Reddit API for social sentiment data
- Yahoo Finance for stock price validation
- VADER Sentiment Analysis library
- The r/WallStreetBets community

## ⚠️ **Disclaimer**

This tool is for educational and research purposes only. Past performance does not guarantee future results. Always do your own research before making investment decisions.

---

**⭐ Star this repository if you find it useful!**

📧 **Contact**: [Your Email] | 🐦 **Twitter**: [@your_handle]
