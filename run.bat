@echo off
cd /d "%~dp0"


:main_loop
python .\main.py

pause

set /p user_input="Press enter to run again or send 'e' to close: "
if /i "%user_input%"=="e" exit /b
goto main_loop
