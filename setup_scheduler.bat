@echo off
REM Task Scheduler Setup Batch File - Run as Administrator

echo ==========================================
echo Stock Sentiment Analysis - Task Scheduler Setup
echo ==========================================
echo.

echo This will set up automated daily runs at 9:00 AM
echo.
echo Prerequisites:
echo - Python installed and in PATH
echo - All project files in current directory
echo.

pause

echo Setting up Task Scheduler...
powershell -ExecutionPolicy Bypass -File "setup_task_scheduler.ps1"

echo.
echo ==========================================
echo Setup complete! Check output above for results.
echo ==========================================

pause
