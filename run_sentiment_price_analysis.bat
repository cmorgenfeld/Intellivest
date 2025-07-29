@echo off
REM Comprehensive Sentiment vs Price Analysis

echo ==========================================
echo Sentiment vs Price Performance Analysis
echo ==========================================
echo.

cd /d "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

echo Running comprehensive sentiment vs price correlation analysis...
echo This will compare historical sentiment data with actual stock price movements.
echo.

REM Run with different time periods
echo Analyzing past 14 days:
python sentiment_price_analyzer.py --days 14

echo.
echo Analyzing past 30 days:
python sentiment_price_analyzer.py --days 30

echo.
echo ==========================================
echo Analysis complete! Check the generated JSON files for detailed results.
echo ==========================================

pause
