@echo off
REM Stock Sentiment Analysis - Status Monitor

echo ==========================================
echo Stock Sentiment Analysis - Status Monitor  
echo ==========================================
echo.

cd /d "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

echo Checking Task Scheduler status...
powershell -Command "Get-ScheduledTaskInfo -TaskName 'StockSentimentAnalysis' | Format-List TaskName, NextRunTime, LastRunTime, LastTaskResult"

echo.
echo Recent Daily Results:
dir daily_results\*.json /O-D | find "analysis_" | head -5

echo.
echo Recent Log Files:  
dir logs\*.log /O-D | find "daily_analysis" | head -3

echo.
echo Latest Analysis Summary:
powershell -Command "python automated_daily_runner.py --summary"

echo.
echo ==========================================
echo Status check complete!
echo ==========================================

pause
