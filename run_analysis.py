"""
Main script to run the complete stock sentiment analysis.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.main import StockSentimentAnalyzer
from src.utils.helpers import setup_directories

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


async def main():
    """Run the complete sentiment analysis pipeline."""
    logger.info("Starting Stock Sentiment Analysis")
    
    try:
        # Setup necessary directories
        setup_directories()
        
        # Initialize and run analyzer
        analyzer = StockSentimentAnalyzer()
        rankings = await analyzer.run_analysis()
        
        # Display top results
        print("\n" + "="*60)
        print("TOP STOCK RANKINGS")
        print("="*60)
        
        for i, stock in enumerate(rankings[:10], 1):
            print(f"{i:2d}. {stock['symbol']:6s} | "
                  f"Score: {stock['composite_score']:6.3f} | "
                  f"Sentiment: {stock['composite_sentiment']:6.3f} | "
                  f"Mentions: {stock['total_mentions']:3d} | "
                  f"Confidence: {stock['confidence_score']:5.3f}")
        
        print("\n" + "="*60)
        print(f"Analysis complete! Analyzed {len(rankings)} stocks.")
        print("Data stored in database for historical tracking.")
        
        return rankings
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise


if __name__ == "__main__":
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Run the analysis
    asyncio.run(main())
