# API Documentation

## Core Classes and Functions

### SentimentAnalyzer (`src/sentiment_analyzer.py`)

The main sentiment analysis engine that processes text from social media posts.

#### Methods

##### `analyze_text(text: str) -> Dict`
Analyzes sentiment of given text using multiple models.

**Parameters:**
- `text` (str): The text to analyze

**Returns:**
- Dict containing:
  - `compound_score` (float): Overall sentiment (-1 to 1)
  - `sentiment` (str): 'positive', 'negative', or 'neutral'
  - `confidence` (float): Confidence level (0 to 1)
  - `details` (dict): Individual model scores

**Example:**
```python
from src.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze_text("TSLA to the moon! 🚀")
print(result['sentiment'])  # 'positive'
print(result['compound_score'])  # 0.8
```

##### `get_model_weights() -> Dict`
Returns current weighting of sentiment models.

### StockRanker (`src/stock_ranker.py`)

Ranks stocks based on aggregated sentiment data.

#### Methods

##### `rank_stocks(days_back: int = 7) -> List[Dict]`
Generates ranked list of stocks based on recent sentiment.

**Parameters:**
- `days_back` (int): Number of days to analyze (default: 7)

**Returns:**
- List of dictionaries with stock rankings

**Example:**
```python
from src.stock_ranker import StockRanker

ranker = StockRanker()
rankings = ranker.rank_stocks(days_back=14)
for stock in rankings[:5]:
    print(f"{stock['symbol']}: {stock['score']:.2f}")
```

### RedditScraper (`src/scrapers/reddit_scraper.py`)

Scrapes Reddit posts from financial subreddits.

#### Methods

##### `scrape_posts(subreddit: str, limit: int = 100) -> List[Dict]`
Scrapes posts from specified subreddit.

**Parameters:**
- `subreddit` (str): Subreddit name (e.g., 'wallstreetbets')
- `limit` (int): Maximum posts to scrape

**Returns:**
- List of post dictionaries

### TwitterScraper (`src/scrapers/twitter_scraper.py`)

Scrapes tweets related to stock symbols.

#### Methods

##### `scrape_tweets(query: str, count: int = 100) -> List[Dict]`
Scrapes tweets matching the query.

**Parameters:**
- `query` (str): Search query
- `count` (int): Maximum tweets to retrieve

**Returns:**
- List of tweet dictionaries

## Database Schema

### Tables

#### `reddit_posts`
```sql
CREATE TABLE reddit_posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT,
    author TEXT,
    created_utc INTEGER,
    score INTEGER,
    num_comments INTEGER,
    url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `tweets`
```sql
CREATE TABLE tweets (
    id TEXT PRIMARY KEY,
    content TEXT,
    author TEXT,
    created_at TIMESTAMP,
    retweet_count INTEGER,
    like_count INTEGER,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `sentiment_analysis`
```sql
CREATE TABLE sentiment_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id TEXT,
    content_type TEXT,
    stock_symbol TEXT,
    sentiment_score REAL,
    sentiment_label TEXT,
    confidence REAL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `stock_rankings`
```sql
CREATE TABLE stock_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    total_mentions INTEGER,
    avg_sentiment REAL,
    confidence_score REAL,
    final_score REAL,
    ranking_date DATE,
    period_days INTEGER
);
```

## Configuration

### API Keys (`config/api_keys.json`)
```json
{
  "reddit": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "user_agent": "your_user_agent"
  },
  "twitter": {
    "bearer_token": "your_bearer_token"
  }
}
```

### Settings (`config/settings.json`)
```json
{
  "analysis": {
    "min_mentions": 5,
    "sentiment_threshold": 0.1,
    "confidence_weight": 0.3
  },
  "scraping": {
    "reddit": {
      "subreddits": ["wallstreetbets", "investing", "stocks"],
      "post_limit": 100
    },
    "twitter": {
      "tweet_limit": 100
    }
  }
}
```

## Error Handling

### Common Exceptions

#### `APIAuthenticationError`
Raised when API credentials are invalid or expired.

```python
try:
    scraper.scrape_posts('wallstreetbets')
except APIAuthenticationError as e:
    print(f"Authentication failed: {e}")
```

#### `RateLimitError`
Raised when API rate limits are exceeded.

```python
try:
    scraper.scrape_tweets('$TSLA')
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    time.sleep(300)  # Wait 5 minutes
```

## Performance Metrics

The system tracks various performance metrics:

### Sentiment Analysis Accuracy
- Historical backtesting shows 43.8% accuracy for 7-day predictions
- Top-mentioned stocks show higher accuracy rates

### Processing Speed
- ~100 Reddit posts: 2-3 seconds
- ~100 Tweets: 3-5 seconds
- Full analysis cycle: 30-60 seconds

### API Rate Limits
- Reddit: 60 requests per minute
- Twitter: Varies by endpoint (300-15 requests per 15 minutes)

## Extending the System

### Adding New Sentiment Models

1. Create a new analyzer class:
```python
class CustomSentimentAnalyzer:
    def analyze(self, text):
        # Your custom logic
        return {
            'score': 0.5,
            'confidence': 0.8
        }
```

2. Register in `SentimentAnalyzer`:
```python
self.custom_analyzer = CustomSentimentAnalyzer()
```

### Adding New Data Sources

1. Create a scraper class following the existing pattern
2. Implement required methods: `scrape_posts()`, `authenticate()`
3. Add to main analysis pipeline

### Custom Stock Filtering

Modify `StockRanker.filter_stocks()` to add custom filtering logic:

```python
def custom_filter(self, stocks):
    # Filter by market cap, sector, etc.
    return filtered_stocks
```
