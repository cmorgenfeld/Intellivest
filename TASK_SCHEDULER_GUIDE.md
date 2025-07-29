# 🤖 Windows Task Scheduler Setup Guide

## Quick Setup (Recommended)

### Option 1: Automated Setup
1. **Right-click** on `setup_scheduler.bat`
2. Select **"Run as Administrator"**
3. Follow the prompts - it will set up everything automatically!

### Option 2: PowerShell Direct
1. **Right-click** on PowerShell and select **"Run as Administrator"**
2. Navigate to your project folder:
   ```powershell
   cd "c:\Users\Creighton\Documents\Automations Work\Investment Ideas"
   ```
3. Run the setup script:
   ```powershell
   .\setup_task_scheduler.ps1
   ```

## Manual Setup (Alternative)

1. **Open Task Scheduler**
   - Press `Windows + R`
   - Type `taskschd.msc` and press Enter

2. **Create Basic Task**
   - Click "Create Basic Task" in the right panel
   - Name: `StockSentimentAnalysis`
   - Description: `Daily automated stock sentiment analysis`

3. **Set Trigger**
   - Select "Daily"
   - Start date: Today's date
   - Start time: `9:00:00 AM` (or your preferred time)
   - Recur every: `1 days`

4. **Set Action**
   - Select "Start a program"
   - Program/script: `python.exe`
   - Add arguments: `automated_daily_runner.py`
   - Start in: `c:\Users\Creighton\Documents\Automations Work\Investment Ideas`

5. **Finish Setup**
   - Check "Open the Properties dialog when I click Finish"
   - In Properties, go to "Settings" tab
   - Check "Allow task to run on batteries"
   - Check "Start the task only if the computer is on AC power" (uncheck this)

## Verify Setup

### Check Task Status
```powershell
Get-ScheduledTask -TaskName "StockSentimentAnalysis"
```

### Test Manual Run
```powershell
Start-ScheduledTask -TaskName "StockSentimentAnalysis"
```

### Monitor Execution
- Check `logs/` folder for execution logs
- Check `daily_results/` folder for analysis outputs

## Troubleshooting

### Common Issues:

**❌ Task shows "Running" but never completes**
- Solution: Check Python path is correct
- Test: Open Command Prompt and type `python --version`

**❌ "Access Denied" errors**
- Solution: Make sure you ran setup as Administrator
- Solution: Check folder permissions

**❌ Task runs but no output files**
- Solution: Check the "Start in" directory is correct
- Solution: Verify all Python dependencies are installed

**❌ Python not found error**
- Solution: Add Python to system PATH
- Or use full Python path: `C:\Users\Creighton\AppData\Local\Microsoft\WindowsApps\python.exe`

### View Task History
1. Open Task Scheduler
2. Navigate to "Task Scheduler Library"
3. Find "StockSentimentAnalysis"
4. Click "History" tab to see execution details

## Schedule Options

### Change Run Time
```powershell
# Example: Change to 8:00 AM
$Task = Get-ScheduledTask -TaskName "StockSentimentAnalysis"
$Task.Triggers[0].StartBoundary = [DateTime]::Today.AddHours(8).ToString("yyyy-MM-ddTHH:mm:ss")
Set-ScheduledTask -InputObject $Task
```

### Multiple Daily Runs
- Modify the setup script to include multiple triggers
- Or manually add additional triggers in Task Scheduler GUI

## Management Commands

### Start/Stop Task
```powershell
Start-ScheduledTask -TaskName "StockSentimentAnalysis"    # Run now
Stop-ScheduledTask -TaskName "StockSentimentAnalysis"     # Stop if running
```

### Enable/Disable Task
```powershell
Enable-ScheduledTask -TaskName "StockSentimentAnalysis"   # Enable
Disable-ScheduledTask -TaskName "StockSentimentAnalysis"  # Disable
```

### Remove Task
```powershell
Unregister-ScheduledTask -TaskName "StockSentimentAnalysis" -Confirm:$false
```

## Expected Behavior

**✅ When Working Correctly:**
- Task runs daily at 9:00 AM
- Creates new JSON file in `daily_results/` folder
- Creates daily log in `logs/` folder  
- Analysis completes in 2-3 minutes
- No user interaction required

**📊 Daily Output:**
- `daily_results/analysis_YYYYMMDD.json` - Analysis results
- `logs/daily_analysis_YYYYMMDD.log` - Execution log
- Updated database with new sentiment data

## Next Steps

1. **Wait 24 hours** for first automated run
2. **Check results** in `daily_results/` folder
3. **Run weekly summary** with `weekly_summary.bat`
4. **Monitor trends** as data accumulates over time

Your stock sentiment analysis will now run automatically every day, building a comprehensive historical dataset for better predictions!
