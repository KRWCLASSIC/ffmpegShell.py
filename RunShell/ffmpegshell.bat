@echo off
setlocal
set "script_dir=%~dp0"
cd /d "%cd%"
python "%script_dir%\..\ffmpegShell.py" %*
endlocal
