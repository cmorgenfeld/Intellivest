# Intellivest Setup Guide

## Prerequisites

- Python 3.11 or higher
- Git
- Windows 10/11 (for Task Scheduler automation)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cmorgenfeld/Intellivest.git
   cd Intellivest
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials:**
   - Copy `config/api_keys_template.json` to `config/api_keys.json`
   - Add your Reddit API credentials:
     ```json
     {
       "reddit": {
         "client_id": "your_reddit_client_id",
         "client_secret": "your_reddit_client_secret",
         "user_agent": "your_reddit_user_agent"
       },
       "twitter": {
         "bearer_token": "your_twitter_bearer_token",
         "api_key": "your_twitter_api_key",
         "api_secret": "your_twitter_api_secret",
         "access_token": "your_twitter_access_token",
         "access_token_secret": "your_twitter_access_token_secret"
       }
     }
     ```

## Getting API Keys

### Reddit API
1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App"
3. Choose "script" application type
4. Note your client_id and client_secret

### Twitter API (Optional)
1. Apply for Twitter API access at [developer.twitter.com](https://developer.twitter.com)
2. Create a new app and generate your API keys
3. Note: The system can run with Reddit only

## Running the System

### Manual Analysis
```bash
python main.py
```

### One-time Comprehensive Analysis
```bash
python automated_daily_runner.py
```

### Historical Backtesting
```bash
python scripts/run_backtesting.py
```

### Price Correlation Analysis
```bash
python sentiment_price_analyzer.py
```

## Windows Task Scheduler Setup

For automated daily analysis:

1. **Run setup script as Administrator:**
   ```powershell
   .\setup_task_scheduler.ps1
   ```

2. **Verify task creation:**
   - Open Task Scheduler
   - Look for "StockSentimentAnalysis" task
   - Task runs daily at 9:00 AM

## Configuration

Edit `config/settings.json` to customize:
- Analysis timeframes
- Stock filtering criteria
- Sentiment thresholds
- Output preferences

## Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure you're running from the project root directory
   - Verify all dependencies are installed

2. **API authentication failures:**
   - Check your API credentials in `config/api_keys.json`
   - Verify API key permissions and rate limits

3. **Task Scheduler issues:**
   - Run PowerShell as Administrator
   - Check Windows Event Viewer for task execution logs

4. **Database errors:**
   - Delete `data/sentiment_analysis.db` to reset
   - The database will be recreated on next run

### Performance Optimization

- The system performs best with at least 4GB RAM
- Historical analysis can take 5-10 minutes depending on data volume
- Consider running analysis during off-market hours for best API performance

## Data Storage

- **Database:** `data/sentiment_analysis.db` (SQLite)
- **Daily Results:** `daily_results/`
- **Logs:** `logs/`
- **Configuration:** `config/`

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in the `logs/` directory
3. Open an issue on GitHub with relevant log excerpts
