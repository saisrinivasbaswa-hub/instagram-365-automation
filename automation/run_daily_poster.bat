@echo off
REM 365-Day Instagram Fully Automated Daily Poster Launcher
cd /d "%~dp0.."
echo [%DATE% %TIME%] Running Instagram Daily Poster... >> "%~dp0poster_log.txt"

python "%~dp0post_via_browser.py" >> "%~dp0poster_log.txt" 2>&1

echo [%DATE% %TIME%] Completed execution. >> "%~dp0poster_log.txt"
