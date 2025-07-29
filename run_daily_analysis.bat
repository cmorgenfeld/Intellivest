@echo off
REM Daily Stock Sentiment Analysis Automation Script
REM Place this in your Windows startup folder or schedule with Task Scheduler

echo ==========================================
echo Stock Sentiment Analysis - Daily Runner
echo ==========================================
echo.

cd /d "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

echo Running daily analysis...
python automated_daily_runner.py

echo.
echo ==========================================
echo Analysis complete! Check daily_results folder for output.
echo ==========================================

pause
