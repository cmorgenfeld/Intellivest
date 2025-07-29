# Task Scheduler Management Commands
# Useful PowerShell commands for managing your automated stock analysis

# ========================================
# TASK MANAGEMENT COMMANDS
# ========================================

# Check if task exists and view details
Get-ScheduledTask -TaskName "StockSentimentAnalysis" | Format-List

# View task history and last run results
Get-ScheduledTaskInfo -TaskName "StockSentimentAnalysis"

# Start the task manually (for testing)
Start-ScheduledTask -TaskName "StockSentimentAnalysis"

# Stop the running task
Stop-ScheduledTask -TaskName "StockSentimentAnalysis"

# Enable the task
Enable-ScheduledTask -TaskName "StockSentimentAnalysis"

# Disable the task (without deleting)
Disable-ScheduledTask -TaskName "StockSentimentAnalysis"

# Delete the task completely
Unregister-ScheduledTask -TaskName "StockSentimentAnalysis" -Confirm:$false

# ========================================
# MONITORING COMMANDS
# ========================================

# Check last 5 runs
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TaskScheduler/Operational'; ID=100,101,102,103,106,107,108,109,110,111,129,140,141,142} | Where-Object {$_.Message -like "*StockSentimentAnalysis*"} | Select-Object -First 5 | Format-Table TimeCreated, Id, LevelDisplayName, Message -Wrap

# View all scheduled tasks
Get-ScheduledTask | Where-Object {$_.State -eq "Ready"} | Sort-Object TaskName

# ========================================
# TROUBLESHOOTING COMMANDS
# ========================================

# Test Python path
python --version
Get-Command python

# Check working directory exists
Test-Path "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"

# List files in project directory
Get-ChildItem "c:\Users\Creighton\Documents\Automations Work\Investment Ideas" -Name

# Check recent log files
Get-ChildItem "c:\Users\Creighton\Documents\Automations Work\Investment Ideas\logs" -Name | Sort-Object -Descending | Select-Object -First 5

# View latest log file
Get-Content "c:\Users\Creighton\Documents\Automations Work\Investment Ideas\logs\daily_analysis_$(Get-Date -Format 'yyyyMMdd').log" -Tail 20

# ========================================
# MODIFY SCHEDULE EXAMPLES
# ========================================

# Change to run at 8:00 AM instead of 9:00 AM
$Task = Get-ScheduledTask -TaskName "StockSentimentAnalysis"
$Task.Triggers[0].StartBoundary = [DateTime]::Today.AddHours(8).ToString("yyyy-MM-ddTHH:mm:ss")
Set-ScheduledTask -InputObject $Task

# Change to run twice daily (8 AM and 6 PM)
# First, remove existing task
Unregister-ScheduledTask -TaskName "StockSentimentAnalysis" -Confirm:$false

# Create new task with multiple triggers
$Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automated_daily_runner.py" -WorkingDirectory "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "8:00AM"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "6:00PM"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName "StockSentimentAnalysis" -Action $Action -Trigger @($Trigger1, $Trigger2) -Settings $Settings -Principal $Principal

Write-Host "📋 Task Scheduler Management Commands Loaded!"
Write-Host "Copy and paste any of the above commands to manage your automated analysis."
