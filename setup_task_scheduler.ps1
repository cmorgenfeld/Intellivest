# Automated Task Scheduler Setup
# Run this PowerShell script as Administrator to set up automated daily runs

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Stock Sentiment Analysis - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Define the task parameters
$TaskName = "StockSentimentAnalysis"
$ScriptPath = "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
$PythonScript = "automated_daily_runner.py"
$LogFile = "$ScriptPath\logs\task_scheduler.log"

Write-Host "Setting up automated daily stock analysis..." -ForegroundColor Yellow
Write-Host "Task Name: $TaskName" -ForegroundColor Green
Write-Host "Script Location: $ScriptPath\$PythonScript" -ForegroundColor Green
Write-Host ""

try {
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($ExistingTask) {
        Write-Host "Task '$TaskName' already exists. Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    # Create the action (what to run)
    $PythonPath = "C:\Users\Creighton\AppData\Local\Microsoft\WindowsApps\python.exe"
    $Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $PythonScript -WorkingDirectory $ScriptPath
    
    # Create the trigger (when to run) - Daily at 9:00 AM
    $Trigger = New-ScheduledTaskTrigger -Daily -At "9:00AM"
    
    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5)
    
    # Create the principal (run as current user)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
    
    # Register the scheduled task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Daily automated stock sentiment analysis using Reddit data"
    
    Write-Host "✅ SUCCESS: Scheduled task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📅 Schedule: Daily at 9:00 AM" -ForegroundColor Cyan
    Write-Host "📁 Working Directory: $ScriptPath" -ForegroundColor Cyan
    Write-Host "🐍 Python Script: $PythonScript" -ForegroundColor Cyan
    Write-Host "📝 Logs will be saved to: $ScriptPath\logs\" -ForegroundColor Cyan
    Write-Host ""
    
    # Show the created task
    Write-Host "Task Details:" -ForegroundColor Yellow
    Get-ScheduledTask -TaskName $TaskName | Format-Table -AutoSize
    
    Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. The task will run automatically every day at 9:00 AM" -ForegroundColor White
    Write-Host "2. Check the logs folder for execution details" -ForegroundColor White
    Write-Host "3. Check daily_results folder for analysis outputs" -ForegroundColor White
    Write-Host "4. Run 'Get-ScheduledTask -TaskName `"$TaskName`"' to check status" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 To modify the schedule:" -ForegroundColor Yellow
    Write-Host "1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
    Write-Host "2. Find '$TaskName' in the Task Scheduler Library" -ForegroundColor White
    Write-Host "3. Right-click and select Properties to modify" -ForegroundColor White
    
} catch {
    Write-Host "❌ ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're running PowerShell as Administrator" -ForegroundColor White
    Write-Host "2. Verify Python is installed and in PATH" -ForegroundColor White
    Write-Host "3. Check that the script path exists" -ForegroundColor White
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
