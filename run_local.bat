@echo off
title Karthik Portfolio - Local Dev Launcher
echo ============================================================
echo   Starting Karthik Portfolio (Frontend + FastAPI Backend)
echo ============================================================
echo.

REM 1. Start FastAPI Backend on Port 8000 in a new window
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Portfolio Backend (FastAPI)" cmd /k "cd /d "%~dp0backend" && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM 2. Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

REM 3. Start Frontend HTTP Server on Port 5500 in a new window
echo [2/2] Starting Frontend Server on http://127.0.0.1:5500 ...
start "Portfolio Frontend" cmd /k "cd /d "%~dp0" && python -m http.server 5500 --bind 127.0.0.1"

REM 4. Open default browser to the portfolio
echo.
echo Launching portfolio in your default browser...
timeout /t 1 /nobreak >nul
start http://127.0.0.1:5500/index.html

echo.
echo ============================================================
echo   Both services are now running!
echo   - Frontend: http://127.0.0.1:5500
echo   - Backend:  http://127.0.0.1:8000
echo   - API Docs: http://127.0.0.1:8000/docs
echo   To stop, simply close the two command windows.
echo ============================================================
pause
