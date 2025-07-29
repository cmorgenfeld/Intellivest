# Automated Stock Sentiment Analysis - Daily Runner
# Schedule this with Windows Task Scheduler or run manually

# For Windows Task Scheduler:
# 1. Open Task Scheduler
# 2. Create Basic Task
# 3. Set trigger to Daily at preferred time (e.g., 9:00 AM)
# 4. Set action to "Start a program"
# 5. Program: C:\Users\Creighton\AppData\Local\Microsoft\WindowsApps\python.exe
# 6. Arguments: "c:\Users\Creighton\Documents\Automations Work\Investment Ideas\automated_daily_runner.py"
# 7. Start in: "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

# For PowerShell scheduled task (run as administrator):
# $action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automated_daily_runner.py" -WorkingDirectory "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
# $trigger = New-ScheduledTaskTrigger -Daily -At 9am
# $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
# Register-ScheduledTask -TaskName "StockSentimentAnalysis" -Action $action -Trigger $trigger -Settings $settings

# Manual run commands:
# cd "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
# python automated_daily_runner.py              # Run daily analysis
# python automated_daily_runner.py --summary    # View weekly summary
# python automated_daily_runner.py --test       # Test mode

# Directory structure created:
# - logs/                    # Daily log files
# - daily_results/          # JSON results for each day
# - data/                   # Database (already exists)

Write-Host "Stock Sentiment Analysis - Automation Setup"
Write-Host "==========================================="
Write-Host ""
Write-Host "To set up automated daily runs:"
Write-Host "1. Task Scheduler (Recommended):"
Write-Host "   - Open Task Scheduler"
Write-Host "   - Create Basic Task"  
Write-Host "   - Set Daily trigger at 9:00 AM"
Write-Host "   - Program: python.exe"
Write-Host "   - Arguments: automated_daily_runner.py"
Write-Host "   - Start in: current directory"
Write-Host ""
Write-Host "2. Manual PowerShell (run as admin):"
Write-Host "   Execute the PowerShell commands in this file"
Write-Host ""
Write-Host "3. Manual runs:"
Write-Host "   python automated_daily_runner.py"
Write-Host "   python automated_daily_runner.py --summary"
