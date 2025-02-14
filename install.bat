@echo off
cd /d "%~dp0"
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is NOT installed
    echo Python is NOT installed
    echo Python is NOT installed
    echo Python is NOT installed
    echo.
    echo Python is NOT installed
    echo make sure to check 'ADD TO PATH' while installing it
    echo make sure to install pip with it 'it will do it by default nowadays'
    echo.
    echo.
    echo just download the last python's last version from its site 
    echo https://www.python.org/downloads/ ctr+click to open in browser
    echo.
    echo it will install the pip too ^(unless you uncheck it manually^)
    pause
    exit \b
)
pip --version >nul 2>&1 
if %errorlevel% neq 0 (
    echo.
    echo pip is NOT installed
    echo.
    echo you can install it by python's last version installer
    echo.
    echo.
    echo just download the last python's last version from its site 
    echo https://www.python.org/downloads/ ctr+click to open in browser
    echo.
    echo it will install the pip too ^(unless you uncheck it manually^)
    pause
    exit \b
)
pip install -r .\req.txt
echo.
echo.
echo DONE
echo.
echo you may now run start.bat
echo.

pause
