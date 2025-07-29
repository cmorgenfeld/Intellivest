@echo off
REM Weekly Summary Report for Stock Sentiment Analysis

echo ==========================================
echo Stock Sentiment Analysis - Weekly Summary
echo ==========================================
echo.

cd /d "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

echo Generating weekly summary...
python automated_daily_runner.py --summary

echo.
echo Generating comprehensive weekly analysis...
python weekly_comprehensive_analysis.py

echo.
echo ==========================================
echo Reports complete!
echo ==========================================

pause
