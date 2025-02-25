@echo off
cd /d "%~dp0"

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo you need to install 'git' to update via this file
    echo otherwise you need to download it manually from https://github.com/Parham-Mehrabi/ielts_practice
    pause
    exit \b
)

git pull origin main

pause