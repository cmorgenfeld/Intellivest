# Stock Sentiment Analysis Project

A web scraper that analyzes sentiment from r/WallStreetBets and Twitter to rank stocks for investment decisions.

## Project Structure

```
├── src/
│   ├── scrapers/
│   │   ├── reddit_scraper.py      # Reddit/WSB scraping functionality
│   │   ├── twitter_scraper.py     # Twitter scraping functionality
│   │   └── __init__.py
│   ├── analysis/
│   │   ├── sentiment_analyzer.py  # Sentiment analysis engine
│   │   ├── stock_ranker.py        # Stock ranking algorithms
│   │   └── __init__.py
│   ├── data/
│   │   ├── database.py            # Database operations
│   │   ├── models.py              # Data models
│   │   └── __init__.py
│   ├── utils/
│   │   ├── config.py              # Configuration management
│   │   ├── helpers.py             # Utility functions
│   │   └── __init__.py
│   └── main.py                    # Main application entry point
├── data/
│   ├── raw/                       # Raw scraped data
│   ├── processed/                 # Processed sentiment data
│   └── results/                   # Stock rankings and reports
├── tests/
│   ├── test_scrapers.py
│   ├── test_analysis.py
│   └── __init__.py
├── config/
│   ├── settings.yaml              # Application settings
│   └── api_keys.env.example       # Example API keys file
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables example
├── .gitignore                     # Git ignore file
└── run_analysis.py                # Script to run the full analysis
```

## Features

- **Reddit Scraping**: Monitors r/WallStreetBets for stock mentions and sentiment
- **Twitter Scraping**: Analyzes stock-related tweets for sentiment
- **Sentiment Analysis**: Uses NLP to determine positive/negative sentiment
- **Stock Ranking**: Combines sentiment data to rank stocks
- **Data Storage**: Stores historical data for trend analysis
- **Configurable**: Easy to modify settings and parameters

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your API keys
3. Configure settings in `config/settings.yaml`
4. Run the analysis: `python run_analysis.py`

## Next Steps

- Implement Reddit scraping functionality
- Add Twitter API integration
- Develop sentiment analysis models
- Create stock ranking algorithms
- Add data visualization and reporting
