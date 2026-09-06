@echo off
echo Setting up 365-Day Instagram Auto-Poster in Windows Task Scheduler...

set SCRIPT_PATH=%~dp0automation\run_daily_background.py
set PYTHON_PATH=python.exe

schtasks /create /tn "Instagram365AutoPoster" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\" --now" /sc daily /st 23:00 /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo SUCCESS! Windows Task Scheduler task 'Instagram365AutoPoster' created!
    echo It will automatically post your daily content every night at 11:00 PM.
    echo ========================================================
) else (
    echo.
    echo Failed to create Task Scheduler task. Try running setup_windows_scheduler.bat as Administrator.
)
pause
