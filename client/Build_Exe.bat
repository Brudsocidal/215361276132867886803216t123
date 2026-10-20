@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher (py.exe) not found. Install Python 3.10-3.12.
  pause
  exit /b 1
)
py -3.12 --version
if errorlevel 1 (
  echo Python 3.12 not found. Edit this script to use an installed supported Python version.
  pause
  exit /b 1
)
py -3.12 -m pip install -r requirements.txt
if errorlevel 1 goto :err
py -3.12 -m PyInstaller --noconfirm --clean delaydame.spec
if errorlevel 1 goto :err
echo Build completed. Test dist\VNDELAY\VNDELAY.exe on a clean Windows machine.
pause
exit /b 0
:err
echo BUILD FAILED. Read the error above.
pause
exit /b 1
