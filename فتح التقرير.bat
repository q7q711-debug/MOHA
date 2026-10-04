@echo off
cd /d "%~dp0"
start "Magrabi report" /min python magrabi-report-server.py
timeout /t 1 /nobreak >nul
start "" "http://127.0.0.1:18923/Magrabi%%20Best%%20Sellers.html"
