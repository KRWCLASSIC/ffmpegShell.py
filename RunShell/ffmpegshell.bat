@echo off
setlocal

rem Find the folder from script is getting executed
set "script_dir=%~dp0"

rem Release Type
set release=standalone

rem Run Depending on Release Type
if "%release%"=="portable" (
    rem This one sets python_exec to script_dir, folder back, and where Portable Python should be. 
    set "python_exec=%script_dir%\..\.ffscore\PortablePython\python.exe"
) else if "%release%"=="standalone" (
    rem This one sets python_exec to just python, this means it will use your installed python (3.11 Recommended). Run ".install_req.bat" before
    set "python_exec=python"
) else (
    rem If you change release type - fuck you
    echo "Release variable is not set or is not recognized."
    timeout -t 3
    exit /b
)

rem Point script_path to main script
set "script_path=%script_dir%\..\ffmpegShell.py"

rem Run whatever was created in this mess passing all arguments along
"%python_exec%" "%script_path%" %*

rem I don't even know if i need this local shit...
endlocal

rem I hate this script deep from my heart...